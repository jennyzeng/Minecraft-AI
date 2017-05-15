import MalmoPython
import os
import sys
import time
import random
import com.microsoft.Malmo.Client

from generateWorldXML import generateXMLbySeed
import random

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
    my_mission_record = MalmoPython.MissionRecordSpec()
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


print "Mission running ",


# If we could change from turning our player in the range 0 to +90 to turning in the range -45 to +45,
# that would fix our problem
#if(randint(0,100)<10):
cc=1
list1=[]

while world_state.is_mission_running:


    cc+=1
    agent_host.sendCommand("move " + str(0.5 * (random.random() * 2 - 0.5)))
    agent_host.sendCommand( "turn " + str(0.5*(random.random()*2-1)) )


    if ((cc % 10) ==0):
        agent_host.sendCommand("fly" + str(0.5 * (random.random() * 2 - 1)))

    time.sleep(1)

    world_state = agent_host.getWorldState()
    list1=world_state.observations

    ct=0

    for i in range(len(list1)):
        if list1[i].equals("lava"):
            ct+=1
            if ct>=4:
                print "Mission ended"
                break




    print "video,observations", world_state.number_of_video_frames_since_last_state, \
        world_state.number_of_observations_since_last_state




print "Mission ended"
# Mission has ended.