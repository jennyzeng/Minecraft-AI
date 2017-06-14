import os
import sys
import time

import MalmoPython

from src.Assets.generateWorldXML import generateXMLbySeed
from src.Img_Preprocess.ImgPreprocess import saveArrayAsImg

# -- set up the mission -- #
# mission_file = './world.xml'
# with open(mission_file, 'r') as f:
#     print "Loading mission from %s" % mission_file
#     mission_xml = f.read()
#     my_mission = MalmoPython.MissionSpec(mission_xml, True)
#     my_mission_record = MalmoPython.MissionRecordSpec()

#add location of ffmpeg. in terminal, put "which ffmpeg" and you will get it
if "/usr/local/bin" not in os.environ["PATH"]:
    os.environ["PATH"] += ":/usr/local/bin"

cur_path = os.getcwd()
### please replace paths below with your FULL PATH to these files in seeds directory
###  to use world setting files
### pay attention to special characters in name (use '\')

biomes = {"desert":str(cur_path)+"/seeds/desert",
          "forest": str(cur_path)+"/seeds/forest",
          "mesa":str(cur_path)+"/seeds/mesa",
          "eh": str(cur_path) + "/seeds/eh",
          "jungle":str(cur_path)+"/seeds/jungle"}
img_width = 320
img_height = 200
weather = 'clear'
# available weather choices: 'normal'|'clear'|'rain'|'thunder'
biome ='eh'
start_time = 0
#0 <= value <= 23999
#choices" 0 = dawn 6000 = noon 18000 = midnight
#pitch_time = [0, 0.5, 1, 2]
weather_list = ['normal','clear','rain','thunder',] #'normal','clear','rain',
time_list = [0, 3000, 6000, 9000, 12000]
biome_list = ["desert", "forest", "mesa", "eh", "jungle"]
entity_list = ['pig','sheep']
entity = 'sheep'
c = 1

for weather in weather_list:
    for start_time in time_list:
        # for pt in pitch_time:
        try:
            missionXML = generateXMLbySeed(biomes[biome], img_width, img_height, weather, start_time, entity)
            my_mission = MalmoPython.MissionSpec(missionXML, True)
            my_mission_record = MalmoPython.MissionRecordSpec("./data.tgz")
            my_mission_record.recordMP4(20, 400000)
            # print my_mission.getVideoWidth()
            # print my_mission.getVideoHeight()
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
                    print "Error starting mission:", e
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
                print "Error:", error.text

        print
        print "Mission running ",
        past_time = time.time()

        while world_state.is_mission_running:
            # time.sleep(random.random())
            # agent_host.sendCommand( "turn " + str(0.5*(random.random()*2-1)) )
            # time.sleep(random.random())
            world_state = agent_host.getWorldState()
            # agent_host.sendCommand("move 2")
            # current_time = time.time()
            # for i in range(10):
            # agent_host.sendCommand("turn -1")
            # agent_host.sendCommand("move 2")
            # agent_host.sendCommand("turn -1")
            # agent_host.sendCommand("turn 1")
            # agent_host.sendCommand("move " + str(0.5 * (random.random() * 100 - 0.5)))
            # agent_host.sendCommand("turn " + str(0.5 * (random.random() * 2 - 1)))
            # time.sleep(0.5)
            # print "finishing sleeping"
            # current_time = time.time()
            # past_time = current_time
            # agent_host.sendCommand("pitch 0.1")
            # time.sleep(0.1)
            # agent_host.sendCommand("pitch 0")

            if world_state.number_of_video_frames_since_last_state > 0:
                cur_time = time.time()
                if cur_time - past_time > 3:
                    print "image to save!"
                    img = world_state.video_frames[-1].pixels
                    saveArrayAsImg(img, img_width, img_height, "./img/" + entity + '_rgb/' + entity +"_"  + str(c) + ".jpg",
                                   "./img/" + entity + '_d/' + entity +"_"  + str(c) + "_d" + ".jpg")
                    c += 1
                    past_time = cur_time

            # print "Mission running "
        print "Mission End"
