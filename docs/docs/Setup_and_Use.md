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
			#		vcan0: 	used for dev on linux and for development
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

#Updating the Beaglebone Black

There are a few different methods to update the beaglebone's software via usb cable. All of the methods below require the use of ssh and are much easier to handle on a linux machine. The automated version requires utilities that are given in a linux os environment so all scripts that need to be run need to run on a Linux machine.

###Connect the Beaglebone Black

The beaglebone black has a mini usb plug (similar to many portable hard drives) on the same side as the network connection on the board. Connect this usb to your computer and wait for the the Beaglebone to boot up (if it was originally off). No other peripheral needs to be connected to the beaglebone black, just the usb cable to the computer.

###Setup beaglebone running environment

Since the environmentConfig.py is not copied to the beaglebone, this needs to be setup manually. To do this, you need to create the file on the beaglebone. 

1. Use the appropriate method to ssh into the board based on your OS (there are lots of tutorials online).
2. Navigate through the command line to the correct folder. This will be located in /home/ubuntu/SAEDashboard/main/.
		
		cd /home/ubuntu/SAEDashboard/main/

	or

		cd ~/SAEDashboard/main/

3. Create or edit the environmentConfig.py file and make the same environmentConfig.py file as you can see on your laptop except with the correct configuration values. These are explained in the code design tab. 

		nano environmentConfig.py

	You can use any command line editor that you prefer whether that be vi, nano, etc.

4. Save the file and 

##__Automatic update__

The automatic update method requires the use of a linux based os running environment. THIS SCRIPT WILL NOT RUN ON WINDOWS.

To automatically update the beaglebone using the included python script updateBeagleBone.py, the only real thing that needs to be done is run the command:

	python3.4 updateBeagleBone.py

This program first checks for beaglebone connectivity before copying the required files to the beaglebone. 

Once the a connection has been established the script prints the files that are being copied and updated on the beaglebone. Files already on the beaglebone will not be deleted. 

####__Common automatic update errors__
If the script is not able to connect to the beaglebone, there are a few common issues.

1. Beaglebone is not connected
2. Beaglebone has not finished booting up (boot should only take 15 to 45 seconds) 
3. There is an issue with the virtual ip address that is set up over the usb cable.

To fix the first two issues, you should reconnect the beaglebone to the computer and wait the required amount of time for the beaglebone to boot. 

If there is an issue with the virtual ip address, there could be a host of other reasons for the inability to connect to the beaglebone. This would require further debugging and probably no small amount of googling. To make sure that there is an issue somewhere with connecting with the beaglebone (as explained later in the manual update method) run this script in linux:

	ping 192.168.7.2

If there is a response than the the beaglebone is properly connected.

If there is an issue with ssh keys or other ssh problems. The script will try to fix this by generating the proper keys and copying them to the beaglebone. You may be prompted for a password for the board, if that is the case:

	Username: ubuntu
	Password: temppwd

Any other issues will need to be handled through the manual method. 

####__Change files that are copied__

To change the files that the automatic updater copies edit the updateBeagleBone.py script's variable:__ignore 

The copy algorithm looks at filenames and directories the same so if the full name is in the __ignore than the file or folder should be ignored. It isn't as sophisticated as the .gitignore system.

##__Manual update__

This process is more advanced and could break the system on the beaglebone. If there are any issues, make sure you take the proper precautions to not delete any files or move any directories. Everything should go smoothly but be warned.. [Enter Pirates of the Caribbean picture here]

###__Linux update__

1. Check that the beaglebone is connected to the computer:

	ping 192.168.7.2

	192.168.7.2 is the virtual ip address that the beaglebone sets up that the computer is able to communicate through. The proper output will show responses like this:
		
		64 bytes from 192.168.7.2: icmp_seq=1 ttl=64 time=0.434 ms
		64 bytes from 192.168.7.2: icmp_seq=2 ttl=64 time=0.272 ms
		64 bytes from 192.168.7.2: icmp_seq=3 ttl=64 time=0.313 ms

	If these are continually displayed, that means that the beaglebone is connected and is ready to be updated.

2. ssh into the beaglebone

		ssh ubuntu@192.168.7.2

	if you run into any issues, there are many helpful tutorials online regarding ssh and how to use it. If you haven't set up for the beaglebone to remember your ssh-key (tutorials on how to do that online) than the credentials to login are:

		username:ubuntu
		password:temppwd

3. Make sure that configuration files are setup (explained earlier)
4. Exit out of the ssh terminal

		exit

5. Start copying files over to the beaglebone.

	The structure will look similar to below but will change for every file that you copy and the destination that you need that file to go.

		scp [/path/to/file/on/your/computer/] ubuntu@192.168.7.2:/home/ubuntu/SAEDashboard/[file or path]

	An example of copying over the dataStore.py file is below

		scp [/path/to/dataStore/dashboard]/main/dataStore.py ubuntu@192.168.7.2:/home/ubuntu/SAEDashboard/main/dataStore.py

	This needs to be done for all the files that have been changed or that need to be updated to the board.

6. You can check your work and make sure the directory didn't get messed up by using ssh to reconnect to the device and checking the file structure/files using
		
		cd

	and

		vi

	or

		nano

7. After everything is working, the python program needs to be restarted either through the restart.py python script, restarting the beaglebone, or by killing the process.

	####__To kill a python process__
	1. Get the PID of all the python processes. The command process will be included in the list, it will have the word __grep__ in the line description.

		ps -ux | grep python3.4

	2. Using all the shown python3.4 process shown from the previous command kill using __pkill__ or any other command that your linux environment uses.

		pkill [PID]

###__Windows update__

There are many ways to ssh into the beaglebone in windows (terminal and graphical) and this will be left up to you. 

Programs like winscp and filezilla might be the easiest to use as graphical interfaces go and that way you can edit and copy whatever files you need. Follow the same type of procedure as in linux (i.e. the updating of files)
