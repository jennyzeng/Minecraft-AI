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
labelp =["no_pig","pig"]
COLOR = ('b','g','r') # channel order in array


nn=1
nnp = 2

recog_pig = False

IMAGE_HEIGHT = 200
IMAGE_WIDTH = 320
NUM_CHANNELS = 3
BATCH_SIZE = 10
cur_path = os.getcwd()


###model for  classsification
pig_file=str(cur_path)+ "/sklearn_model/weather.pkl"
pig_model = joblib.load(pig_file)



### CNN model for biome classification
checkpoint_file = str(cur_path)+ "/model/biome_model/model.ckpt"
### CNN model for pig classification
pig_checkpoint_file = str(cur_path) + "/model/pig_model2/pig_model.ckpt"




biomes = {"desert":str(cur_path)+"/seeds/desert",
          "forest": str(cur_path)+"/seeds/forest",
          "mesa":str(cur_path)+"/seeds/mesa",
          "eh": str(cur_path) + "/seeds/eh",
          "jungle":str(cur_path)+"/seeds/jungle"}

biomes_for_pig_rec = {"forest": str(cur_path)+"/seeds/forest",
                      "eh": str(cur_path) + "/seeds/eh"}

record_height = 200
record_width = 320
sess = None


#helper function

def convertImage(img,label,NUM_BINS,COLOR):
   # img=cv2.imread(img_path)
   # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hist = np.zeros((NUM_BINS,5))
    bins = np.linspace(0, 256, NUM_BINS)
    for i,col in enumerate(COLOR):
        histr = cv2.calcHist([img],[i],None,[NUM_BINS],[0,256])
        hist[:,i] = histr[:,0]
    hist = hist.flatten()
    hist = np.append(hist, label)
    return hist

def convertLabel(lab):
    return (np.arange(5) == lab[:, None]).astype(np.float32)

def convertLabelp(labp):
    return (np.arange(2) == labp[:, None]).astype(np.float32)


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
    print "init biome model"
    model_pig = import_graph.ImportGraph(pig_checkpoint_file)
    print "init pig model"

    test_data_node = model_biome.graph.get_operation_by_name("test_data_node").outputs[0]

    test_prediction = model_biome.graph.get_operation_by_name("test_prediction").outputs[0]

    pig_test_data_node = model_pig.graph.get_operation_by_name("test_data_node").outputs[0]
    pig_test_prediction = model_pig.graph.get_operation_by_name("test_prediction").outputs[0]


except Exception as e:
    if model_pig.sess:
        model_pig.close()

    if model_biome.sess:
        model_biome.close()


    print "Tensorflow init session ERROR:", e
    exit(0)






try:
    missionXML = generateXMLbySeed(biomes[labels[nn]],record_width,record_height,'normal','6000','pig')
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


counter=0
correct1=0
correct2=0

while world_state.is_mission_running:
    world_state = agent_host.getWorldState()
    if len(world_state.observations) >0:
        print str(world_state.observations[-1])
    if world_state.number_of_video_frames_since_last_state > 0:
        pixels = world_state.video_frames[-1].pixels
        batch_data.append(scaleImg(pixels,IMAGE_HEIGHT, IMAGE_WIDTH, record_height, record_width))
    if len(batch_data) == BATCH_SIZE:
        img_list = np.array(batch_data)



        ###
        # This is CNN
        print "batch size biome"
        predictions = model_biome.run([test_prediction],
                                   feed_dict={test_data_node: batch_data})[0]
        predictions = np.argmax(predictions, 1)
        predictions_p = model_pig.run([pig_test_prediction], feed_dict={pig_test_data_node: batch_data})[0]
        predictions_p = np.argmax(predictions_p, 1)
        print "tf predictions: ", predictions
        maj = np.bincount(predictions).argmax()
        print "maj for now:", labels[maj]
        print "tf predictions of pig: ", predictions_p
        #agent_host.sendCommand("chat from tensorflow. this is: {}".format(labels[maj]))
        batch_data = []
        if (labels[maj]==labels[nn]):
            correct1+=1

        counter = counter + 1
            #print correct1, counter
            #print

            ####

        ####traditional ML:

        data = np.array([convertImage(img_dir, nn, BATCH_SIZE, COLOR) for img_dir in img_list])

        np.random.shuffle(data)
        X = data[:, :-1]
        Y = data[:, -1].astype(np.int64)
        forest = RandomForestClassifier(n_estimators=100, random_state=1)
        multi_target_forest = MultiOutputClassifier(forest, n_jobs=3)
        predictions1 = multi_target_forest.fit(X, convertLabel(Y)).predict(X)

        predictions1 = np.argmax(predictions1, 1)
        print "RF predictions: ", predictions1
        maj1 = np.bincount(predictions1).argmax()
        print "maj for now:", labels[maj1]


        agent_host.sendCommand("chat from Random Forest. this is: {}".format(labels[maj1]))

        ###error rate
        if (labels[maj1] == labels[nn]):
            correct2 = correct2 + 1



        err1 = float(counter-correct1) / float(counter)
        err2 = float(counter-correct2) / float(counter)
        agent_host.sendCommand("chat Current error rate for CNN: {}% ".format(err1))
        agent_host.sendCommand("chat Current error rate for Random Forest: {}% ".format(err2))
        ###













    time.sleep(0.1)

###error rate

err3 = (counter-correct1) / counter
err4 = (counter-correct2) / counter
print "Total error rate for CNN: {}% ".format(err3)
print "Total error rate for Random Forest: {}% ".format(err4)
###

model_pig.close()
model_biome.close()

