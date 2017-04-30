"""
try different settings on
http://minecraft.tools/en/custom.php?#seed
"""
import random


def generateXMLbySeed(seedfile):
	xpos = int((random.random() - 0.5) * 20000)
	zpos = int((random.random() - 0.5) * 20000)
	missionXML = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
	<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

	  <About>
	    <Summary>Generate biome for video record Schema</Summary>
	  </About>

	  <ServerSection>
	    <ServerInitialConditions>
	        <Time><StartTime>1</StartTime></Time>
	    </ServerInitialConditions>
	    <ServerHandlers>
	      <FileWorldGenerator src="{src}" forceReset="1" destroyAfterUse="1"/>
	      <ServerQuitFromTimeUp timeLimitMs="5000"/>
	      <ServerQuitWhenAnyAgentFinishes/>
	    </ServerHandlers>
	  </ServerSection>

	  <AgentSection mode="Spectator">
	                <Name>MalmoBot</Name>
	                <AgentStart>
			    <Placement x="''' + str(xpos + 0.5) + '''" y="1.0" z="''' + str(zpos + 0.5) + '''"/>
	                    <!--<Placement x="0.5" y="100.0" z="0.5" yaw="90"/>-->
	                </AgentStart>
	                <AgentHandlers>
	                <VideoProducer
					want_depth="0"
					viewpoint="2">
					<Width> {width} </Width>
					<Height> {height} </Height>
					</VideoProducer>
	                  <ObservationFromFullStats/>
	                  <ContinuousMovementCommands turnSpeedDegs="180"/>
	                </AgentHandlers>
	              </AgentSection>

	</Mission>
	'''
	return missionXML.format(src=srcfile, width=width, height= height)
