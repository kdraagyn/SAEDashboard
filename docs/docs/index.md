# Installation Process

To install everything on a windows machine:
	
1. Install Python3.4
		</br><blockquote><a href="https://www.python.org/downloads/release/python-340/">Download Python3.4</a></blockquote>

2. Download and install the python-can library
		</br><blockquote><a href="https://bitbucket.org/hardbyte/python-can/downloads">Download python-can</a></blockquote>

3. Download and install the pySerial library
		</br><blockquote><a href="https://pypi.python.org/pypi/pyserial/2.7">Download pySerial</a></blockquote>

4. Create a "environmentConfig.py" file in the dashboard folder with these lines of code:

	###environmentConfig.py
		class environment:
			# set to "True" whenever you need to work with the GUI and random numbers should be generated
			# set to "False" whenever the can bus should be read
			guiDev = False

			# set interface to listen to for can messages
			# 	vcan0: 	used for dev on linux and for development
			#		can0:		used for actual hardware messages and the production configuration
			bus = "vcan0"

			# absolute location of frames declaration file
			framesFileDeclaration = "/path/to/canids.xml"

			DEV = "dev"  # on restart both will
			DASH = "dash"
			PUSH = "push"

			# environment type 
			envType = DEV

	This file only tells the program to configure environment to automatically generate random values, set can input type and set the canids.xml location

5. Now start editing gauges.py and widgetComiler.py to create custom gauges

## Project layout

    .gitignore    # git ignore file for use by git repository
    readme.txt
    restart.py
    <updateBeagleBone class="py"></updateBeagleBone>
    main/
        canids.xml
    tools/
    		can0.sh