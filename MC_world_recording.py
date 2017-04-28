import MalmoPython
import os
import sys
import time
from generateWorldXML import generateXMLbySeed
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

try:

    missionXML = generateXMLbySeed(biomes["mesa"])
    my_mission = MalmoPython.MissionSpec(missionXML, True)
    my_mission_record = MalmoPython.MissionRecordSpec()
    my_mission_record.recordMP4(1,100000)
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


agent_host.sendCommand("fly 1")
# time.sleep(1)
agent_host.sendCommand("pitch 0.2")
time.sleep(1)
agent_host.sendCommand("pitch 0")

# agent_host.sendCommand("jump 0")
# Loop until mission ends:
while world_state.is_mission_running:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:",error.text

print
print "Mission ended"
# Mission has ended.