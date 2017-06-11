from src.Assets.generateWorldXML import generateXMLbySeed
from src.Reg_Malmo import import_graph

import MalmoPython
import os
import sys
import time
record_height = 200
record_width = 320
proj_path = "set here"

biomes = {"desert": str(proj_path) + "/src/Assets/seeds/desert",
          "forest": str(proj_path) + "/src/Assets/seeds/forest",
          "mesa": str(proj_path) + "/src/Assets/seeds/mesa",
          "eh": str(proj_path) + "/src/Assets/seeds/eh",
          "jungle": str(proj_path) + "/src/Assets/seeds/jungle"}

labels = ["mesa", "forest", "desert", "jungle", "eh"]
labelp = ["no_pig", "pig"]
COLOR = ('b', 'g', 'r')  # channel order in array
labelw = ['normal', "rain", "thunder"]





biomes_for_pig_rec = {"forest": str(proj_path) + "/src/Assets/seeds/forest",
                      "eh": str(proj_path) + "/src/Assets/seeds/eh"}




def init_tf_model(checkpoint_files):
	model_list = []
	test_data_node_list = []
	test_prediction_list = []
	for ckp in checkpoint_files:
		try:
			model = import_graph.ImportGraph(ckp)
			test_data_node = model.graph.get_operation_by_name("test_data_node").outputs[0]
			test_prediction = model.graph.get_operation_by_name("test_prediction").outputs[0]
			model_list.append(model)
			test_data_node_list.append(test_data_node)
			test_prediction_list.append(test_prediction)
		except Exception as e:
			if model.sess:
				model.close()
			print "Tensorflow init session ERROR:", e
			exit(0)
	return model_list, test_data_node_list, test_prediction_list


def init_mission(nn, weather, time, entity):
	try:
		missionXML = generateXMLbySeed(biomes[labels[nn]], record_width, record_height, weather, time, entity)
		my_mission = MalmoPython.MissionSpec(missionXML, True)
		my_mission_record = MalmoPython.MissionRecordSpec('./data.tgz')
		my_mission_record.recordMP4(20, 400000)
		return my_mission, my_mission_record
	except Exception as e:
		print "open mission ERROR: ", e


def init_agent():
	agent_host = MalmoPython.AgentHost()
	try:
		agent_host.parse(sys.argv)
		return agent_host
	except RuntimeError as e:
		print 'ERROR:', e
		print agent_host.getUsage()
		exit(1)
	if agent_host.receivedArgument("help"):
		print agent_host.getUsage()
		exit(0)

def start_mission(agent_host,my_mission, my_mission_record):
	# Attempt to start a mission:
	max_retries = 3
	for retry in range(max_retries):
		try:
			agent_host.startMission(my_mission, my_mission_record)
			break
		except RuntimeError as e:
			if retry == max_retries - 1:
				print "Error starting mission:", e
				exit(1)
			else:
				time.sleep(2)

def wait_till_start(agent_host):

	# Loop until mission starts:
	print "Waiting for the mission to start ",
	world_state = agent_host.getWorldState()
	while not world_state.has_mission_begun:
		sys.stdout.write(".")
		time.sleep(0.1)
		world_state = agent_host.getWorldState()

		for error in world_state.errors:
			print "Error:", error.text

	print
	print "Mission running ",
