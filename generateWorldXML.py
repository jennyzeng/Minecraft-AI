"""
try different settings on
http://minecraft.tools/en/custom.php?#seed
"""



def generateXMLbySeed(srcfile, width, height):
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
	                    <!--<Placement x="0.5" y="100" z="0.5" yaw="90"/>-->
	                </AgentStart>
	                <AgentHandlers>
	                <VideoProducer
					want_depth="1"
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
