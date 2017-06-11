import tensorflow as tf
import numpy as np
import os
from generateWorldXML import generateXMLforClassification
from generateWorldXML import generateXMLbySeed
import MalmoPython
import sys
import time
import cv2
from sklearn.datasets import make_regression
from sklearn.datasets import make_classification
from sklearn.multioutput import MultiOutputRegressor
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle
import numpy as np
import glob
from sklearn.externals import joblib
import import_graph

# config tf
if 'TF_CPP_MIN_LOG_LEVEL' not in os.environ:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from MC_Img_Preprocess import scaleImg

#add location of ffmpeg. in terminal, put "which ffmpeg" and you will get it
if "/usr/local/bin" not in os.environ["PATH"]:
    os.environ["PATH"] += ":/usr/local/bin"


labels =["mesa", "forest","desert","jungle", "eh"]
labelp =["None","Pig","Chicken","Cow"]
COLOR = ('b','g','r') # channel order in array
labelw = ['normal',"rain", "thunder"]


nn=1
nnp = 2
nnw = 0

recog_pig = False

IMAGE_HEIGHT = 200
IMAGE_WIDTH = 320
NUM_CHANNELS = 3
BATCH_SIZE = 10
cur_path = os.getcwd()


###sklearn model for animal classsification
rf_animal_file= str(cur_path) + "/sklearn_model/animal.pkl"
rf_animal_model = joblib.load(rf_animal_file)

rf_biome_file = str(cur_path) + "/sklearn_model/biome.pkl"
rf_biome_model = joblib.load(rf_biome_file)

rf_weather_file = str(cur_path) + '/sklearn_model/weather.pkl'
rf_weather_model = joblib.load(rf_weather_file)


### CNN model for biome classification
checkpoint_file = str(cur_path)+ "/model/biome_model/model.ckpt"
### CNN model for pig classification
pig_checkpoint_file = str(cur_path) + "/model/pig_model/pig_model.ckpt"
weather_checkpoint_file = str(cur_path) + "/model/weather_model2_no_normal/weather_model.ckpt"




biomes = {"desert":str(cur_path)+"/seeds/desert",
          "forest": str(cur_path)+"/seeds/forest",
          "mesa":str(cur_path)+"/seeds/mesa",
          "eh": str(cur_path) + "/seeds/eh",
          "jungle":str(cur_path)+"/seeds/jungle"}

biomes_for_pig_rec = {"forest": str(cur_path)+"/seeds/forest",
                      "eh": str(cur_path) + "/seeds/eh"}



record_height = 400
record_width = 640
sess = None


#helper function

def convertImage(img,label,NUM_BINS,COLOR):
   # img=cv2.imread(img_path)
   # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hist = np.zeros((NUM_BINS,3))
    bins = np.linspace(0, 256, NUM_BINS)
    for i,col in enumerate(COLOR):
        histr = cv2.calcHist([img],[i],None,[NUM_BINS],[0,256])
        hist[:,i] = histr[:,0]
    hist = hist.flatten()
    hist = np.append(hist, label)
    return hist

def convertLabel(lab, num_labels=5):
    return (np.arange(num_labels) == lab[:, None]).astype(np.float32)



def error_rate(predictions, labels):
   # Return the error rate and confusions.
    correct = np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1))
    total = predictions.shape[0]

    error = 100.0 - (100 * float(correct) / float(total))

    confusions = np.zeros([5, 5], np.float32)
    bundled = zip(np.argmax(predictions, 1), np.argmax(labels, 1))
    for predicted, actual in bundled:
        confusions[predicted, actual] += 1

    return error, confusions



print('Done')


#####

try:
    model_biome = import_graph.ImportGraph(checkpoint_file)
    #print "init biome model"
    model_pig = import_graph.ImportGraph(pig_checkpoint_file)
    print "init pig model"
    model_weather = import_graph.ImportGraph(weather_checkpoint_file)
    print "init weather model"

    test_data_node = model_biome.graph.get_operation_by_name("test_data_node").outputs[0]
    test_prediction = model_biome.graph.get_operation_by_name("test_prediction").outputs[0]

    pig_test_data_node = model_pig.graph.get_operation_by_name("test_data_node").outputs[0]
    pig_test_prediction = model_pig.graph.get_operation_by_name("test_prediction").outputs[0]

    weather_test_data_node = model_weather.graph.get_operation_by_name("test_data_node").outputs[0]
    weather_test_prediction = model_weather.graph.get_operation_by_name("test_prediction").outputs[0]

except Exception as e:
    if model_weather.sess:
        model_weather.close()

    if model_pig.sess:
        model_pig.close()
    #
    if model_biome.sess:
         model_biome.close()


    print "Tensorflow init session ERROR:", e
    exit(0)






try:
    missionXML = generateXMLbySeed(biomes[labels[nn]],record_width,record_height,labelw[nnw],'6000','pig')
    my_mission = MalmoPython.MissionSpec(missionXML, True)
    my_mission_record = MalmoPython.MissionRecordSpec('./data.tgz')
    my_mission_record.recordMP4(20, 400000)
except Exception as e:
    print "open mission ERROR: ", e

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse(sys.argv)
except RuntimeError as e:
    print 'ERROR:', e
    print agent_host.getUsage()
    exit(1)
if agent_host.receivedArgument("help"):
    print agent_host.getUsage()
    exit(0)


# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission(my_mission, my_mission_record)
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print "Error starting mission:",e
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print "Waiting for the mission to start ",
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()



    for error in world_state.errors:
        print "Error:",error.text

print
print "Mission running ",
batch_data = []
batch_data_p = []


counter=0
correct = 0
correct1=0
correct2=0
correct3 = 0

BATCH_SIZE_P = 5

while world_state.is_mission_running:
    world_state = agent_host.getWorldState()
    if world_state.number_of_video_frames_since_last_state > 0:
        pixels = world_state.video_frames[-1].pixels
        batch_data.append(scaleImg(pixels,IMAGE_HEIGHT, IMAGE_WIDTH, record_height, record_width))

    if len(batch_data) == BATCH_SIZE:
        img_list = np.array(batch_data)






        ###
        # This is CNN
        predictions = model_biome.run([test_prediction],
                                    feed_dict={test_data_node: batch_data})[0]
        predictions = np.argmax(predictions, 1)
        predictions_p = model_pig.run([pig_test_prediction], feed_dict={pig_test_data_node: batch_data[:5]})[0]
        predictions_p = np.argmax(predictions_p, 1)
        predictions_w = model_weather.run([weather_test_prediction], feed_dict={weather_test_data_node:batch_data})[0]
        predictions_w = np.argmax(predictions_w, 1)
        # print "tf predictions: ", predictions
        maj = np.bincount(predictions).argmax()
        print "maj for now:", labels[maj]
        print "tf predictions of pig: ", predictions_p
        print "tf prediction of weather", predictions_w
        maj_w = np.bincount(predictions_w).argmax()
        maj_p = np.bincount(predictions_p).argmax()
        #agent_host.sendCommand("chat from tensorflow. this is: {}".format(labels[maj]))

        batch_data = []
        if (labels[maj]==labels[nn]):
            correct1+=1


        # if (labelp[maj_p] == labels[nnp]):
        #     correct2 = correct2 + 1

        if (labelw[maj_w] == labelw[nnw]):
            correct2 = correct2 + 1




        counter = counter + 1

        print "error rate calc"
        print correct2, counter
            #print

            ####

        ####traditional ML:
        #data = np.array([convertImage(img_dir, nn, 8, COLOR) for img_dir in img_list])

        #X = data[:, :-1]
        #Y = data[:, -1].astype(np.int64)

        ###biome

        # predictionsb = rf_biome_model.predict(X)
        # predictionsb = np.argmax(predictionsb, 1)
        # print "RF predictions: ", predictionsb
        # majb = np.bincount(predictionsb).argmax()
        # print "maj for now:", labels[majb]



        ##weather

        # predictionsw = rf_weather_model.predict(X)
        #
        # predictionsw = np.argmax(predictionsw, 1)
        # print "RF predictions of weather: ", predictionsw
        # majw = np.bincount(predictionsw).argmax()
        # print "maj for now:", labelw[majw]majw


        ##animal
        # predictionsp= rf_animal_model.predict(X)
        #
        # predictionsp = np.argmax(predictionsp, 1)
        # print "RF predictions of pig: ", predictionsp
        # majp= np.bincount(predictionsp).argmax()
        # print "maj for now:", labelp[majp]


        ##send chat
        ##biome
        agent_host.sendCommand("chat from CNN biome prediction. this is: {}".format(labels[maj]))
        #agent_host.sendCommand("chat from Random Forest. this is: {}".format(labels[majb]))

        #weather
        agent_host.sendCommand("chat from CNN weather prediction. this is: {}".format(labelw[maj_w]))
        #agent_host.sendCommand("chat from Random Forest weather prediction. this is: {}".format(labelw[majw]))

        #animal
        if labelp[maj_p] != 0:
            agent_host.sendCommand("chat from CNN animal prediction. this is: {}".format(labelp[maj_p]))
        #agent_host.sendCommand("chat from Random Forest animal prediction. this is: {}".format(labelp[majp]))

        ###error rate

        ##biome error rate




        err1 = float(counter-correct1) / float(counter)
        err2 = float(counter-correct2) / float(counter)
        # err3 = float(counter-correct3) / float(counter)
        # #print err1
        print "This is biome CNN error rate  ", err1
        print "This is weather CNN error rate  ", err2


        agent_host.sendCommand("chat Current error rate for CNN biome prediction : {}% ".format(err1))
        agent_host.sendCommand("chat Current error rate for CNN weather prediction: {}% ".format(err2))
        #agent_host.sendCommand("chat Current error rate for CNN weather prediction: {}%".format(err3))
        ###













    time.sleep(0.1)

###error rate
print counter
print correct2
err3 = (counter-correct1) / counter
err4 = (counter-correct2) / counter
print "Total error rate for CNN: {}% ".format(err3)
print "Total error rate for Random Forest: {}% ".format(err4)
###
model_weather.close()
model_pig.close()
model_biome.close()

