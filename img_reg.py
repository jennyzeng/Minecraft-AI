import tensorflow as tf
import numpy as np
import os
from generateWorldXML import generateXMLforClassification
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

def convertLabel(lab):
    return (np.arange(3) == lab[:, None]).astype(np.float32)


def error_rate(predictions, labels):
    """Return the error rate and confusions."""
    correct = np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1))
    total = predictions.shape[0]

    error = 100.0 - (100 * float(correct) / float(total))

    confusions = np.zeros([NUM_LABELS, NUM_LABELS], np.float32)
    bundled = zip(np.argmax(predictions, 1), np.argmax(labels, 1))
    for predicted, actual in bundled:
        confusions[predicted, actual] += 1

    return error, confusions

print('Done')

#####


COLOR = ('b','g','r') # channel order in array
IMG_DIR_PATH = [('/notebooks/Minecraft-AI/mc-data/mesa_splited/**/*.jpg',0),
               ('/notebooks/Minecraft-AI/mc-data/forest_splited/**/*.jpg',1),
               ('/notebooks/Minecraft-AI/mc-data/desert_splited/**/*.jpg',2),
               ('/notebooks/Minecraft-AI/mc-data/jungle_splited/**/*.jpg', 3),
               ('/notebooks/Minecraft-AI/mc-data/eh_splited/**/*.jpg',4)]
FILE_SAVE_PATH = '/notebooks/Minecraft-AI/mc-data/mesa_forest_desert_jungle_eh.txt'
#labels ={"mesa":0, "forest":1, "desert":2, 'jungle':3,"eh":4}
labels =["mesa", "forest","desert","jungle", "eh"]

IMAGE_HEIGHT = 200
IMAGE_WIDTH = 320
NUM_CHANNELS = 3
BATCH_SIZE = 10
cur_path = os.getcwd()
checkpoint_file = str(cur_path)+ "/model/model.ckpt"
biomes = {"desert":str(cur_path)+"/seeds/desert",
          "forest": str(cur_path)+"/seeds/forest",
          "mesa":str(cur_path)+"/seeds/mesa",
          "eh": str(cur_path) + "/seeds/eh",
          "jungle":str(cur_path)+"/seeds/jungle"}

record_height = 400
record_width = 640
sess = None

#####

# config tf
if 'TF_CPP_MIN_LOG_LEVEL' not in os.environ:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from MC_Img_Preprocess import scaleImg

#add location of ffmpeg. in terminal, put "which ffmpeg" and you will get it
if ":/usr/local/bin" not in os.environ["PATH"]:
    os.environ["PATH"] += ":/usr/local/bin"




try:
    # tf session
    sess = tf.InteractiveSession()
    sess.as_default()
    saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
    saver.restore(sess, checkpoint_file)
    tf.global_variables_initializer().run()
    graph = tf.get_default_graph()
    test_data_node = graph.get_operation_by_name("test_data_node").outputs[0]
    test_prediction = graph.get_operation_by_name("test_prediction").outputs[0]

except Exception as e:
    if sess:
        sess.close()
        print "tf sess closed"
    print "Tensorflow init session ERROR:", e
    exit(0)

print test_data_node




try:
    missionXML = generateXMLforClassification(biomes['eh'],record_width,record_height)
    my_mission = MalmoPython.MissionSpec(missionXML, True)
    my_mission_record = MalmoPython.MissionRecordSpec("./data.tgz")
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
        agent_host.startMission( my_mission, my_mission_record )
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
while world_state.is_mission_running:
    world_state = agent_host.getWorldState()
    if world_state.number_of_video_frames_since_last_state > 0:
        pixels = world_state.video_frames[-1].pixels
        subdir=scaleImg(pixels,IMAGE_HEIGHT, IMAGE_WIDTH, record_height, record_width)
        batch_data.append(subdir)
        #sk_data.append(extracted_features(pixels))
        # pixels, extract



    if len(batch_data) == BATCH_SIZE:
        img_list = np.array(batch_data)
       # print img_list.shape,batch_data.shape


        # use traditional ML:
        data = np.array([convertImage(img_dir, 4, BATCH_SIZE, COLOR) for img_dir in img_list])
        np.random.shuffle(data)
        X = data[:, :-1]
        Y = data[:,-1].astype(np.int64)
        forest = RandomForestClassifier(n_estimators=100, random_state=1)
        multi_target_forest = MultiOutputClassifier(forest, n_jobs=3)
        predictions = multi_target_forest.fit(X, convertLabel(Y)).predict(X)
        error_rate(predictions,4);

        #This is CNN
        #predictions=np.argmax(predictions, 1)

        #predictions = sess.run([test_prediction],
                             # feed_dict={test_data_node: batch_data})[0]
        ####

        predictions = np.argmax(predictions, 1)

        print "tf predictions: ", predictions
        maj = np.bincount(predictions).argmax()
        print "maj for now:", labels[maj]
        agent_host.sendCommand("chat from tensorflow. this is: {}".format(labels[maj]))
        batch_data = []
    time.sleep(0.1)

sess.close()