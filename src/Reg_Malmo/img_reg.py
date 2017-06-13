from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from src.Reg_Malmo.helper import *
from src.Img_Preprocess.MC_Img_Preprocess import scaleImg
from sklearn.externals import joblib



target_biome_label = 4
target_weather_label = 1

recog_pig = False

IMAGE_HEIGHT = 200
IMAGE_WIDTH = 320
NUM_CHANNELS = 3
BATCH_SIZE = 10
proj_path = '/Users/xinshen/Documents/school_work/CS175/Malmo-0.21.0-Mac-64bit/Minecraft-AI'


### CNN model for biome classification
biome_checkpoint_file = str(proj_path) + "/model/biome_model/model.ckpt"
### CNN model for pig classification
pig_checkpoint_file = str(proj_path) + "/model/pig_model/pig_model.ckpt"
weather_checkpoint_file = str(proj_path) + "/model/weather_model2_no_normal/weather_model.ckpt"

sess = None

[model_biome, model_pig, model_weather], \
[test_data_node, pig_test_data_node, weather_test_data_node], \
[test_prediction, pig_test_prediction, weather_test_prediction] = init_tf_model(
	[biome_checkpoint_file, pig_checkpoint_file, weather_checkpoint_file])

my_mission, my_mission_record = init_mission(target_biome_label, target_weather_label, '6000', 'pig')
agent_host = init_agent()
start_mission(agent_host,my_mission, my_mission_record)
wait_till_start(agent_host)

counter = 0
correct1 = 0
correct2 = 0
world_state = agent_host.getWorldState()
batch_data = []
while world_state.is_mission_running:
	world_state = agent_host.getWorldState()
	if world_state.number_of_video_frames_since_last_state > 0:
		pixels = world_state.video_frames[-1].pixels
		batch_data.append(scaleImg(pixels, IMAGE_HEIGHT, IMAGE_WIDTH, record_height, record_width))
	if len(batch_data) == BATCH_SIZE:
		img_list = np.array(batch_data)

		###
		# This is CNN
		predictions = model_biome.run([test_prediction],
		                              feed_dict={test_data_node: batch_data})[0]
		predictions = np.argmax(predictions, 1)
		predictions_p = model_pig.run([pig_test_prediction], feed_dict={pig_test_data_node: batch_data[:5]})[0]
		predictions_p = np.argmax(predictions_p, 1)
		predictions_w = model_weather.run([weather_test_prediction], feed_dict={weather_test_data_node: batch_data})[0]
		predictions_w = np.argmax(predictions_w, 1)
		print "tf predictions of biome: ", predictions
		maj = np.bincount(predictions).argmax()
		#print "maj for now:", labels[maj]
		print "tf predictions of pig: ", predictions_p
		print "tf prediction of weather", predictions_w
		maj_w = np.bincount(predictions_w).argmax()
		maj_p = np.bincount(predictions_p).argmax()
		# agent_host.sendCommand("chat from tensorflow. this is: {}".format(labels[maj]))
		batch_data = []
		if (labels[maj] == labels[target_biome_label]):
			correct1 += 1
		if (labelw[maj_w] == labelw[target_weather_label]):
			correct2 += 1

		counter = counter + 1
		# print correct1, counter
		# print

		####

		####traditional ML:

		# data = np.array([convertImage(img_dir, target_biome_label, BATCH_SIZE, COLOR) for img_dir in img_list])
        #
		# np.random.shuffle(data)
		# X = data[:, :-1]
		# Y = data[:, -1].astype(np.int64)
		# forest = RandomForestClassifier(n_estimators=100, random_state=1)
		# multi_target_forest = MultiOutputClassifier(forest, n_jobs=3)
		# predictions1 = multi_target_forest.fit(X, convertLabel(Y)).predict(X)

		# predictions1 = np.argmax(predictions1, 1)
		# print "RF predictions: ", predictions1
		# maj1 = np.bincount(predictions1).argmax()
		# print "maj for now:", labels[maj1]

		agent_host.sendCommand("chat from CNN Biome prediction this is: {}".format(labels[maj]))
		#agent_host.sendCommand("chat from Random Forest. this is: {}".format(labels[maj1]))
		agent_host.sendCommand("chat from CNN weather prediction. this is: {}".format(labelw[maj_w]))
		agent_host.sendCommand("chat from CNN animal prediction. this is: {}".format(labelp[maj_p]))

		###error rate
		# if (labels[maj1] == labels[target_biome_label]):
		# 	correct2 = correct2 + 1

		err1 = float(counter - correct1) / float(counter)
		err2 = float(counter - correct2) / float(counter)
		agent_host.sendCommand("chat Current error rate for CNN biome: {}% ".format(err1))
		agent_host.sendCommand("chat Current error rate for CNN weather: {}% ".format(err2))
		###

	time.sleep(0.1)

###error rate

err3 = (counter - correct1) / counter
err4 = (counter - correct2) / counter
print "Total error rate for CNN biome prediction: {}% ".format(err3)
print "Total error rate for CNN weather prediction: {}% ".format(err4)
###
model_weather.close()
model_pig.close()
model_biome.close()
