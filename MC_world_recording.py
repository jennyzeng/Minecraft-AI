import MalmoPython
import os
import sys
import time
import random
from generateWorldXML import generateXMLbySeed
from MC_Img_Preprocess import saveArrayAsImg
# -- set up the mission -- #
# mission_file = './world.xml'
# with open(mission_file, 'r') as f:
#     print "Loading mission from %s" % mission_file
#     mission_xml = f.read()
#     my_mission = MalmoPython.MissionSpec(mission_xml, True)
#     my_mission_record = MalmoPython.MissionRecordSpec()


### please replace paths below with your FULL PATH to these files in seeds directory
###  to use world setting files
### pay attention to special characters in name (use '\')

biomes = {"desert":"D:\Minecraft-AI\seeds\desert",
          "forest": "D:\Minecraft-AI\seeds\\forest",
          "mesa":"D:\Minecraft-AI\seeds\mesa",
          "eh":"D:\Minecraft-AI\seeds\eh",
          "jungle":"D:\Minecraft-AI\seeds\jungle"}
img_width = 320
img_height = 200
try:

    missionXML = generateXMLbySeed(biomes["mesa"],img_width,img_height)
    my_mission = MalmoPython.MissionSpec(missionXML, True)
    my_mission_record = MalmoPython.MissionRecordSpec("./data.tgz")
    my_mission_record.recordMP4(20, 400000)
    #print my_mission.getVideoWidth()
    #print my_mission.getVideoHeight()
except Exception as e:
    print "open mission ERROR: ", e


agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv)
except RuntimeError as e:
    print 'ERROR:',e
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
c = 1
while world_state.is_mission_running:
    agent_host.sendCommand("move "+ str((random.random() * 10 - 0.5)))
    time.sleep(random.random())
    agent_host.sendCommand( "turn " + str(0.5*(random.random()*2-1)) )
    time.sleep(random.random())
    world_state = agent_host.getWorldState()
    if world_state.number_of_video_frames_since_last_state > 0:
        print "image to save!"
        img = world_state.video_frames[-1].pixels
        saveArrayAsImg(img, img_width, img_height,"./img/test"+str(c)+".jpg")
        c+=1


    for error in world_state.errors:
          print "Error:",error.text

print
print "Mission ended"
# Mission has ended.