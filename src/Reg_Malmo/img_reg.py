from src.Reg_Malmo.helper import Init_Helper as IH
from src.Reg_Malmo.helper import ML_Helper as MH
from src.Img_Preprocess.MC_Img_Preprocess import scaleImg
import numpy as np
import time


class Tintin:
    # Malmo Config
    REG_PIG = False
    RECORD_HEIGHT = 400
    RECORD_WIDTH = 640

    # training config
    IMAGE_HEIGHT = 200
    IMAGE_WIDTH = 320
    NUM_CHANNELS = 3

    def __init__(self, rec_config, targets):
        """
        :param rec_config: recognition type configurations
        :param targets: target configuration
        """
        # init CNN models
        self.models = {}
        for k, v in rec_config.items():
            model, node, pre = IH.init_tf_model(v['ckpt'])
            self.models[k] = {'model': model, 'node': node, 'prediction': pre,
                              'batch_size': v['batch_size'], 'labels': v['labels'],
                              'err': [] # if correct, append 1, else 0

                              }
        self.targets = targets
        # init Malmo mission
        self.my_mission, self.my_mission_record = IH.init_mission(self.RECORD_WIDTH, self.RECORD_HEIGHT,
                                                        self.targets['rec_type']['biome'][0],
                                                        self.targets['rec_type']['weather'][0],
                                                        self.targets['time'], self.targets['rec_type']['animal'][0])
        self.agent_host = IH.init_agent()
        IH.start_mission(self.agent_host, self.my_mission, self.my_mission_record)
        IH.wait_till_start(self.agent_host)
        self.batch_data = []


    def make_prediction(self, batch_data, rec_type):
        model = self.models[rec_type]
        predictions = model['model'].run([model['prediction']],
                                         feed_dict={model['node']: batch_data})[0]
        predictions = np.argmax(predictions, 1)
        print rec_type + ": ", predictions
        maj = MH.find_maj(predictions)
        if maj:
            self.agent_host.sendCommand(
                "chat {rtype}. this is: {label}".format(rtype=rec_type,
                                                        label=model['labels'][maj]))
        return maj

    def single_run(self, world_state):
        """
        handle the situation when we get a new world_state
        :param world_state: current world_state
        """

        if world_state.number_of_video_frames_since_last_state > 0:
            pixels = world_state.video_frames[-1].pixels
            self.batch_data.append(scaleImg(pixels, self.IMAGE_HEIGHT, self.IMAGE_WIDTH,
                                       self.RECORD_HEIGHT, self.RECORD_WIDTH))

        for rec_type, model in self.models.items():
            if len(self.batch_data) == model[rec_type]['batch_size']:
                maj = self.make_prediction(self.batch_data, rec_type)
                if maj:
                    model['err'].append(
                        model['labels'][maj] != self.targets['rec_type'][rec_type][1])
                    err = model['err']
                    err_rate = MH.array_err_rate(err)
                    self.agent_host.sendCommand("chat {rtype} "
                                                "err_rate: {err_rate}".format(rtype=rec_type,err_rate=err_rate))

        if len(self.batch_data) == self.targets['max_batch_size']:
            self.batch_data = []


    def _close_models(self):
        for rec_type, model in self.models.items():
            model['model'].close()
            print "{rtype} is closed".format(rtype=rec_type)

    def main(self):
        world_state = self.agent_host.getWorldState()
        while world_state.is_mission_running:
            world_state = self.agent_host.getWorldState()
            self.single_run(world_state)
            time.sleep(0.1)
        print """\n
        ----------------------------------
        |       total error rates        |
        ----------------------------------
        """
        for rec_type, model in self.models.items():
            err =  model['err']
            err_rate = MH.array_err_rate(err)
            print "{rtype}: {err_rate}".format(rtype=rec_type, err_rate=err_rate)


        self._close_models()


if __name__ == '__main__':
    proj_path = '~/Dropbox/cs/CS175/groupProject'

    rec_config = {"biome": {"ckpt": proj_path + "/model/biome_model/model.ckpt",
                            "labels": ["mesa", "forest", "desert", "jungle", "eh"],
                            "batch_size": 10},
                  "animal": {"ckpt":proj_path + "/model/pig_model/pig_model.ckpt",
                             "labels": ["None", "Pig", "Chicken", "Cow"],
                             "batch_size": 5},
                  "weather": {'ckpt':proj_path+ "/model/weather_model2_no_normal/weather_model.ckpt",
                              "labels": ['normal', "rain", "thunder"],
                              "batch_size": 10}}
    targets = { "rec_type":{
                    "biome": ("forest", 4),
                    "weather": ("clear", 0),
                    "animal": ("pig", 1)},
                "time": "6000",
                "rec_pig": True,
                'max_batch_size': 10
                }

    tintin = Tintin(rec_config,targets)