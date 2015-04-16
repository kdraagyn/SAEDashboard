#Helper Programs and Scripts to help with development

All of these tools can only be used in the linux environment as they all automate tasks needed during development and there was never a need to get work all of these out in any other operating system. If there is a need to work these out in another OS there needs to be more work to port over their functionality to windows or the other operating system that is being used.

##can0.sh

__Requires sudo access__

Script that sets up the can0 network. Sets the can name to can0, type can, and bitrate to 250000 bits/sec.

After this script is run by running:

	ifconfig can0

There should be information regarding the CAN bus. If the can0 network is not initialized than this sort of error will be displayed:

	can0: error fetching interface information: Device not found


##pushCan.py

Use is described in the Setup and Use tab of the documentation. 

This program requires that the vcan0 or can0 interface is up and the environment configuration is setup correctly as it pulls the bus configuration from the configuration file. 

Every command that pushes multiple parameters to the can bus spawns a new sub process that is constantly sending data. 

##vcan0.sh

__Requires sudo access__

Script that sets the vcan0 network. Sets the can name to vcan0, type can, and bitrate to 250000 bits/sec.

To check that the script ran correctly and setup the can interface correctly follow the same procedure as from the documentation in can0.sh

##restart.py

Used by the beaglebone environment to restart the correct python processes. It pulls the environment type from environmentConfig.py to figure out which programs to start. The environment types are described in the __code design__ section.

##updateBeaglebone.py

Python script used to update Beaglebone from another linux computer. This method use is better described in the Setup and Use section of the docs.