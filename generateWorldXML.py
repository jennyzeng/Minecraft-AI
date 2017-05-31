"""
try different settings on
http://minecraft.tools/en/custom.php?#seed
"""
import random

# This tests the force-loading by running missions with random start points (x and z vary between +- 10000),
def generateXMLforClassification(seedfile, width, height):
	xpos = int((random.random() - 0.5) * 20000)
	zpos = int((random.random() - 0.5) * 20000)
	missionXML = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
	<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
	  <About>
		<Summary>Tensorflow biome recognition</Summary>
	  </About>
	  <ServerSection>
		<ServerInitialConditions>
			<Time><StartTime>1</StartTime></Time>
		</ServerInitialConditions>
		<ServerHandlers>
		  <FileWorldGenerator src="{src}" forceReset="1" destroyAfterUse="1"/>
		  <ServerQuitFromTimeUp timeLimitMs="50000"/>
		  <ServerQuitWhenAnyAgentFinishes/>
		</ServerHandlers>
	  </ServerSection>
	  <AgentSection mode="Spectator">
					<Name>MalmoBot</Name>
					<AgentStart>
				<Placement x="''' + str(xpos + 0.5) + '''" y="80.0" z="''' + str(zpos + 0.5) + '''"/>
						<!--<Placement x="0.5" y="100.0" z="0.5" yaw="90"/>-->
					</AgentStart>
					<AgentHandlers>
					<VideoProducer
					want_depth="0"
					viewpoint="0">
					<Width> {width} </Width>
					<Height> {height} </Height>
					</VideoProducer>
					  <ObservationFromFullStats/>
					<ChatCommands/>
					</AgentHandlers>
				  </AgentSection>
	</Mission>
	'''
	return missionXML.format(src=seedfile, width=width, height=height)


# This tests the force-loading by running missions with random start points (x and z vary between +- 10000),
def generateXMLbySeed(seedfile,width,height,weather,start_time,entity):
	xpos = int((random.random() - 0.5) * 20000)
	zpos = int((random.random() - 0.5) * 20000)
	missionXML = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
	<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
	  <About>
	    <Summary>Generate biome for video record Schema</Summary>
	  </About>
	  <ServerSection>
	    <ServerInitialConditions>
	        <Time><StartTime>{start_time}</StartTime>
	        <AllowPassageOfTime>1</AllowPassageOfTime></Time>
	    <Weather>{weather}</Weather>
	    </ServerInitialConditions>
	    <ServerHandlers>
	    <!--   <FileWorldGenerator src="{src}" forceReset="1" destroyAfterUse="1"/> -->

	      <FlatWorldGenerator generatorString="3;minecraft:bedrock,2*minecraft:dirt,minecraft:grass;1;village"/>
            <DrawingDecorator>
                <!-- Tricks to clean the map before drawing (avoid entity duplication on the map) -->
                <!-- coordinates for cuboid are inclusive -->
                <DrawCuboid x1="-10" y1="4" z1="-10" x2="10" y2="45" z2="10" type="air"/>

                <!-- Area Limits -->
                <DrawLine x1="1" y1="3" z1="0" x2="7" y2="3" z2="0" type="sand"/>
                <DrawLine x1="1" y1="4" z1="0" x2="7" y2="4" z2="0" type="fence"/>

                <DrawLine x1="1" y1="3" z1="6" x2="7" y2="3" z2="6" type="sand"/>
                <DrawLine x1="1" y1="4" z1="6" x2="7" y2="4" z2="6" type="fence"/>

                <DrawLine x1="1" y1="3" z1="0" x2="1" y2="3" z2="2" type="sand"/>
                <DrawLine x1="1" y1="4" z1="0" x2="1" y2="4" z2="2" type="fence"/>
                <DrawLine x1="0" y1="3" z1="2" x2="0" y2="3" z2="4" type="sand"/>
                <DrawLine x1="0" y1="4" z1="2" x2="0" y2="4" z2="4" type="fence"/>
                <DrawLine x1="1" y1="3" z1="4" x2="1" y2="3" z2="6" type="sand"/>
                <DrawLine x1="1" y1="4" z1="4" x2="1" y2="4" z2="6" type="fence"/>

                <DrawLine x1="7" y1="3" z1="0" x2="7" y2="3" z2="2" type="sand"/>
                <DrawLine x1="7" y1="4" z1="0" x2="7" y2="4" z2="2" type="fence"/>
                <DrawLine x1="8" y1="3" z1="2" x2="8" y2="3" z2="4" type="sand"/>
                <DrawLine x1="8" y1="4" z1="2" x2="8" y2="4" z2="4" type="fence"/>
                <DrawLine x1="7" y1="3" z1="4" x2="7" y2="3" z2="6" type="sand"/>
                <DrawLine x1="7" y1="4" z1="4" x2="7" y2="4" z2="6" type="fence"/>

                <!-- Path blocker -->
                <DrawBlock x="3" y="3" z="2" type="sand"/>
                <DrawBlock x="3" y="4" z="2" type="fence"/>

                <DrawBlock x="3" y="3" z="4" type="sand"/>
                <DrawBlock x="3" y="4" z="4" type="fence"/>

                <DrawBlock x="5" y="3" z="2" type="sand"/>
                <DrawBlock x="5" y="4" z="2" type="fence"/>

                <DrawBlock x="5" y="3" z="4" type="sand"/>
                <DrawBlock x="5" y="4" z="4" type="fence"/>

                <DrawBlock x="1" y="3" z="3" type="lapis_block"/>
                <DrawBlock x="7" y="3" z="3" type="lapis_block"/>

                <!-- Pig -->
                <DrawEntity x="4.5" y="4" z="3.5" type="Pig"/>

            </DrawingDecorator>
            <ServerQuitFromTimeUp timeLimitMs="80000"/>
            <ServerQuitWhenAnyAgentFinishes/>

	    </ServerHandlers>
	  </ServerSection>
	  <AgentSection mode="Spectator">
	                <Name>MalmoBot</Name>
	                <AgentStart>
					 <Placement x="3" y="6" z="5" pitch="30" yaw="0"/>
			  <!--   <Placement x="4.5" y="5" z="3.5"/>
	                    <Placement x="4.5" y="4" z="3.5" yaw="90"/>-->
	                </AgentStart>
	                <AgentHandlers>
	                <VideoProducer
					want_depth="1"
					viewpoint="0">
					<Width> {width} </Width>
					<Height> {height} </Height>
					</VideoProducer>
	                  <ObservationFromFullStats/>
	                </AgentHandlers>
	              </AgentSection>
	</Mission>
	'''
	return missionXML.format(src=seedfile, width=width, height= height, weather = weather, start_time = start_time, entity = entity)