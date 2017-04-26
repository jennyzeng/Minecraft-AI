import MalmoPython
import os
import sys
import time
from generateWorldXML import generateXMLbySeed
from MC_Img_Preprocess import saveArrayAsImg
# -- set up the mission -- #
# mission_file = './world.xml'
# with open(mission_file, 'r') as f:
#     print "Loading mission from %s" % mission_file
#     mission_xml = f.read()
#     my_mission = MalmoPython.MissionSpec(mission_xml, True)
#     my_mission_record = MalmoPython.MissionRecordSpec()
biomes = {"desert":"./seeds/desert.txt",
          "forest": "./seeds/forest.txt",
          "mesa":"./seeds/mesa.txt",
          "eh":"./seeds/extremeHills.txt",
          "jungle":"./seeds/jungle.txt"}

try:

    missionXML = generateXMLbySeed(biomes["mesa"])
    my_mission = MalmoPython.MissionSpec(missionXML, True)
    my_mission_record = MalmoPython.MissionRecordSpec("./data.tgz")
    my_mission_record.recordMP4(20, 400000)
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
        # agent_host.setVideoPolicy(MalmoPython.AgentHost.VideoPolicy())
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

# agent_host.sendCommand("jump 1")
# agent_host.sendCommand("jump 0")
# agent_host.sendCommand("jump 1")
# agent_host.sendCommand("jump 0")
# agent_host.sendCommand("jump 1")

agent_host.sendCommand("fly 1")
# time.sleep(1)
agent_host.sendCommand("pitch 0.2")
time.sleep(1)
agent_host.sendCommand("pitch 0")
img = world_state.video_frames
print "type img", len(img)
# agent_host.sendCommand("jump 0")
# Loop until mission ends:
while world_state.is_mission_running:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    if world_state.number_of_video_frames_since_last_state > 0:
        img = world_state.video_frames[-1].pixels
        saveArrayAsImg(img, "./img/test.jpg")

    for error in world_state.errors:
        print "Error:",error.text

print
print "Mission ended"
# Mission has ended.