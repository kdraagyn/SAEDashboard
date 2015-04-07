## Libraries Used


## Install on Windows
1. Install Python3.4
	
	<blockquote><a href="https://www.python.org/downloads/release/python-340/">Download Python3.4</a></blockquote>

2. Download and install the python-can library
	
	<blockquote><a href="https://bitbucket.org/hardbyte/python-can/downloads">Download python-can</a></blockquote>

3. Download and install the pySerial library
	
	<blockquote><a href="https://pypi.python.org/pypi/pyserial/2.7">Download pySerial</a></blockquote>

4. Create a "environmentConfig.py" file in the dashboard folder with these lines of code

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

##Install on Linux

This install process is completely within the Linux terminal. You can use the download links above in the Windows installation process to download/unzip the files and then use the Linux terminal.s

1. Install python3.4	
		
		sudo apt-get install python3.4

2. Install pySerial
	In order to make sure it is installed into the python3.4 environment we need to download the source library and install it manually.

		wget https://pypi.python.org/packages/source/p/pyserial/pyserial-2.7.tar.gz

	This will download the zipped pySerial python library source files. They need to be unzipped and run 
		
		gunzip pyserial-2.7
		cd pyserial-2.7
	
	To finally install pySerial run the setup.py file with python3.4 within the pyserial-2.7 directory

		udo python3.4 setup.py install



3. Install python-can
	
	Download zipped source files
	
		wget https://bitbucket.org/hardbyte/python-can/get/11c0cb8e8cb0.zip

	Unzip into python-can Directory

		unzip 11c0cb8e8cb0.zip

	Install from source into python3.4 environment

		cd hardbyte-python-can-11c0cb8e8cb0/
		sudo python3.4 setup-py install

	Create a .canrc file in the home directory. A ~/.canrc file looks like this:
	
		[default]
		interface = socketcan_native
		channel = vcan0

4. Install tkinter

		sudo apt-get install python3-tk

5. Create a "environmentConfig.py" file in the dashboard folder with these lines of code

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

#Project File Structure
	  main/
	      canids.xml
	      config.py
	      dashExceptions.py
	      dataStore.py
	      enviromentConfig.py
	      gauges.py
	      mainRunner.py
	      Wid
	  tools/
	  		can0.sh
	  		pushCan.py
	  		vcan0.sh
	  .gitignore    # git ignore file for use by git repository
	  restart.py
	  updateBeagleBone.py

#Running the Environment

###Environment Config 
When a script is run, the environmentConfig class is used to aid in development control how the application acts 

- <strong>guiDev</strong>: Used to help with gui dev on windows environments get rid of the need for a can bus in gui design
	
	- True: Random value generation

	- False: Listens to CAN bus for values

- <strong>bus</strong>: system name of the can bus network to listen to

- <strong>framesFileDeclaration</strong>: conids.xml location

- <strong>envType</strong>: environment type controls what programs get restarted when restart.py is run. This is only run by the beaglebone whenever the beaglebone is updated and restarted

	- <strong>DEV</strong>: both GUI and pushCan are restarted 

	- <strong>GUI</strong>: only GUI main runner is restarted

	- <strong>PUSH</strong>: only CAN pusher program is restarted

###Run the GUI application
	
In the main/ directory run the main runner python script:

	python3.4 mainRunner.py

###Run the ECU can simulator
	
In the root directory run the pushCan python script as a module:

	python3.4 -m tools.pushCan
