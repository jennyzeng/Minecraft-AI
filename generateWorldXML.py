"""
try different settings on
http://minecraft.tools/en/custom.php?#seed
"""



def generateXMLbySeed(srcfile):
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
	      <ServerQuitFromTimeUp timeLimitMs="50000"/>
	      <ServerQuitWhenAnyAgentFinishes/>
	    </ServerHandlers>
	  </ServerSection>

	  <AgentSection mode="Spectator">
	                <Name>MalmoBot</Name>
	                <AgentStart>
	                    <!--<Placement x="0.5" y="100.0" z="0.5" yaw="90"/>-->
	                </AgentStart>
	                <AgentHandlers>
	                  <ObservationFromFullStats/>
	                  <ContinuousMovementCommands turnSpeedDegs="180"/>
	                </AgentHandlers>
	              </AgentSection>

	</Mission>
	'''
	# src = open(srcfile,'r').read()
	# src = src.replace("\"", "'")
	return missionXML.format(src=srcfile)
