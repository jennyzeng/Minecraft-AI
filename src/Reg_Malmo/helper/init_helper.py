from src.Assets.generateWorldXML import XML_Generator
from src.Reg_Malmo import import_graph
import MalmoPython
import sys
import time

class Init_Helper:

    def __init__(self, proj_path):
        self.proj_path = proj_path
        self.biomes = {"desert": str(proj_path) + "/src/Assets/seeds/desert",
                  "forest": str(proj_path) + "/src/Assets/seeds/forest",
                  "mesa": str(proj_path) + "/src/Assets/seeds/mesa",
                  "eh": str(proj_path) + "/src/Assets/seeds/eh",
                  "jungle": str(proj_path) + "/src/Assets/seeds/jungle"}
        self.biomes_for_pig_rec = {"forest", "eh"}


    def init_tf_model(self, checkpoint_file):
        print "init tf models....",checkpoint_file
        model = None
        try:
            model = import_graph.ImportGraph(checkpoint_file)
            test_data_node = model.graph.get_operation_by_name("test_data_node").outputs[0]
            test_prediction = model.graph.get_operation_by_name("test_prediction").outputs[0]
            print "init tf models succeeded"
            return model, test_data_node, test_prediction
        except Exception as e:
            print "Tensorflow init session ERROR:", e
            if model and model.sess:
                model.close()
            exit(0)

    def init_sk_model(self, pkl_file):
        from sklearn.externals import joblib
        print "init sk learn models", pkl_file
        try:
            model = joblib.load(pkl_file)
            print "init sk learn models succeeded"
            return model
        except Exception as e:
            print "sk init session ERROR: ", e



    def init_mission(self, summary, record_width, record_height, target_biome, weather, time, entity):
        try:
            print "init mission..."
            missionXML = XML_Generator.generateXMLbySeed(summary, self.biomes[target_biome],
                                           record_width, record_height, weather, time, entity)
            my_mission = MalmoPython.MissionSpec(missionXML, True)
            my_mission_record = MalmoPython.MissionRecordSpec('./data.tgz')
            my_mission_record.recordMP4(20, 400000)
            print "init mission succeeded"
            return my_mission, my_mission_record
        except Exception as e:
            print "open mission ERROR: ", e

    def init_agent(self):
        print "init agent host..."
        try:
            agent_host = MalmoPython.AgentHost()
            agent_host.parse(sys.argv)
            print "init agent host succeeded"
            return agent_host
        except RuntimeError as e:
            print 'ERROR:', e
            print agent_host.getUsage()
            exit(1)
        if agent_host.receivedArgument("help"):
            print agent_host.getUsage()
            exit(0)

    def start_mission(self, agent_host, my_mission, my_mission_record):
        # Attempt to start a mission:
        print "start mission..."
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

    def wait_till_start(self, agent_host):
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
