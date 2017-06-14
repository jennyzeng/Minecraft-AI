from src.Reg_Malmo.helper import Init_Helper
from src.Reg_Malmo.helper import ML_Helper as MH
from src.Img_Preprocess.ImgPreprocess import resizeImg, rescaleImg, imgHistograms
import numpy as np
import time
from collections import OrderedDict
import os
from src.Reg_Malmo.helper import MissionHelper

proj_path = MissionHelper.get_grand_parent_path(os.getcwd())
IH = Init_Helper(proj_path)

class Tintin:
    # Malmo Config
    RECORD_HEIGHT = 400
    RECORD_WIDTH = 640

    # training config
    IMAGE_HEIGHT = 200
    IMAGE_WIDTH = 320
    NUM_CHANNELS = 3

    def __init__(self, summary, rec_config, targets):
        '''
        :param rec_config: recognition type configurations
        :param targets: target configuration

        model structure:
        recognition type
                batch_size
                labels
                cnn
                    model
                    node
                    prediction
                    err : a list storing the error count
                sk
                    model
                    err

        '''

        # init models
        self.has_cnn = False
        self.has_sk = False
        self.models = OrderedDict()
        for k, v in rec_config.items():
            self.models[k] = {'batch_size': v['batch_size'], 'labels': v['labels']}
            if 'ckpt' in v:
                model, node, pre = IH.init_tf_model(v['ckpt'])  # CNN
                self.models[k].update({'cnn': {'model': model, 'node': node, 'prediction': pre,
                                               'err': []}})
                self.has_cnn = True
            if 'pkl' in v:
                sk_model = IH.init_sk_model(v['pkl'])  # SK
                self.models[k].update({'sk': {'model': sk_model, 'err': []}})
                self.has_sk = True

        self.targets = targets
        # init Malmo mission
        self.my_mission, self.my_mission_record = IH.init_mission(summary, self.RECORD_WIDTH, self.RECORD_HEIGHT,
                                                                  self.targets['rec_type']['biome'][0],
                                                                  self.targets['rec_type']['weather'][0],
                                                                  self.targets['time'],
                                                                  self.targets['rec_type']['animal'][0])
        self.agent_host = IH.init_agent()
        IH.start_mission(self.agent_host, self.my_mission, self.my_mission_record)
        IH.wait_till_start(self.agent_host)

    def get_maj(self, rec_type, predictions, model_type):
        maj = MH.find_maj(predictions)
        if maj != None:
            self.agent_host.sendCommand(
                'chat {mtype} {rtype} is: {label}'.format(
                    mtype=model_type,
                    rtype=rec_type,
                    label=self.models[rec_type]['labels'][maj]))
        return maj

    def SK_prediction(self, sk_batch_data, rec_type):
        model = self.models[rec_type]['sk']
        predictions = model['model'].predict(sk_batch_data)
        # print "predictions: ", predictions
        predictions = np.argmax(predictions, 1)
        print 'sk ' + rec_type + ': ', predictions
        return self.get_maj(rec_type, predictions, 'sk')

    def CNN_prediction(self, cnn_batch_data, rec_type):
        model = self.models[rec_type]['cnn']
        predictions = model['model'].run([model['prediction']],
                                         feed_dict={model['node']: cnn_batch_data})[0]

        predictions = np.argmax(predictions, 1)
        print "cnn " + rec_type + ': ', predictions
        return self.get_maj(rec_type, predictions, 'cnn')

    def model_err_handler(self, model_name, maj, rec_type):
        if maj == None:
            return
        self.models[rec_type][model_name]['err'].append(
            maj != self.targets['rec_type'][rec_type][1])
        err = self.models[rec_type][model_name]['err']
        err_rate = MH.array_err_rate(err)
        message = '{mtype} {rtype} err_rate: {err_rate}'.format(mtype=model_name,
                                                                rtype=rec_type,
                                                                err_rate=err_rate)
        self.agent_host.sendCommand('chat {message}'.format(message=message))

    def CNN_single_run(self, cnn_batch_data, rec_type):
        maj = self.CNN_prediction(cnn_batch_data, rec_type)
        self.model_err_handler('cnn', maj, rec_type)

    def SK_single_run(self, sk_batch_data, rec_type):
        maj = self.SK_prediction(sk_batch_data, rec_type)
        self.model_err_handler('sk', maj, rec_type)

    def single_run(self, world_state, cnn_batch_data=None, sk_batch_data=None):
        '''
        handle the situation when we get a new world_state
        :param world_state: current world_state
        '''

        if world_state.number_of_video_frames_since_last_state > 0:
            pixels = world_state.video_frames[-1].pixels
            resized_img = resizeImg(pixels, self.IMAGE_HEIGHT, self.IMAGE_WIDTH,
                                    self.RECORD_HEIGHT, self.RECORD_WIDTH)
            if cnn_batch_data != None:
                cnn_batch_data.append(rescaleImg(resized_img))
            if sk_batch_data != None:
                sk_batch_data.append(imgHistograms(resized_img))

        for rec_type, values in self.models.items():
            if cnn_batch_data and len(cnn_batch_data) == values['batch_size']:
                self.CNN_single_run(cnn_batch_data, rec_type)

            if sk_batch_data and len(sk_batch_data) == values['batch_size']:
                self.SK_single_run(sk_batch_data, rec_type)

        if cnn_batch_data and len(cnn_batch_data) == self.targets['max_batch_size']:
            cnn_batch_data = []

        if sk_batch_data and len(sk_batch_data) == self.targets['max_batch_size']:
            sk_batch_data = []
        return cnn_batch_data, sk_batch_data

    def err_beauty_print(self, rec_type, model_name, err):
        err_rate = MH.array_err_rate(err)
        return '{mtype} {rtype}: {err_rate:10.4f}'.format(
            mtype=model_name, rtype=rec_type, err_rate=err_rate)

    def main(self):
        world_state = self.agent_host.getWorldState()
        cnn_batch_data = [] if self.has_cnn else None
        sk_batch_data = [] if self.has_sk else None
        while world_state.is_mission_running:
            world_state = self.agent_host.getWorldState()
            cnn_batch_data, sk_batch_data = self.single_run(world_state, cnn_batch_data, sk_batch_data)
            time.sleep(0.1)

        print '''\n
        ----------------------------------
        |       total error rates        |
        ----------------------------------
        '''
        for rec_type, values in reversed(self.models.items()):
            if 'cnn' in values:
                print '        | ' + self.err_beauty_print(rec_type, 'cnn', values['cnn']['err'])
                values['cnn']['model'].close()

                print '{rtype} model closed'.format(rtype=rec_type)

            if 'sk' in values:
                print '        | ' + self.err_beauty_print(rec_type, 'sk', values['sk']['err'])


if __name__ == '__main__':


    rec_config = {'biome': {
        # 'ckpt': proj_path + '/mo del/biome_model/model.ckpt',
        'pkl': proj_path + '/sk_model/biome.pkl',
        'labels': ['mesa', 'forest', 'desert', 'jungle', 'eh'],
        'batch_size': 10},
        # 'animal': {'ckpt':proj_path + '/model/pig_model/pig_model.ckpt',
        #             'pkl': proj_path + '/sk_model/animal.pkl',
        #            'labels': ['None', 'Pig', 'Chicken', 'Cow'],
        #            'batch_size': 5},
        'weather': {
            # 'ckpt': proj_path + '/model/weather_model/weather_model.ckpt',
            'pkl': proj_path + '/sk_model/weather.pkl',
            'labels': ['normal', 'rain', 'thunder'],
            'batch_size': 10}}
    targets = {'rec_type': {
        'biome': ('desert', 2),
        'weather': ('rain', 1),
        'animal': ('pig', 1)},
        'time': '6000',
        'max_batch_size': 10
    }

    tintin = Tintin('image recognition session',
                    rec_config, targets)
    tintin.main()
