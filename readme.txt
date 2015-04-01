Formula SAE Dashboard Project
Team Members: Keith Nygaard, Grant Spencer, Colin Royston, Kendall Samuel, Corbin Smith

python libraries needed to install:
	tkinter
	serial (pyserial)
	can (python-can)
		make sure there is a .canrc file in the home directory. A ~/.canrc file looks like this:
			[default]
			interface = socketcan_native
			channel = vcan0

To see how to declare a new gauge interface look at the gauges.py file. I commented out directions the textGauge

To install everything on a windows machine:
	
	1. Install Python3.4
		https://www.python.org/downloads/release/python-340/

	2. Download and install the python-can library
		https://bitbucket.org/hardbyte/python-can/downloads

	3. Download and install the pySerial library
		https://pypi.python.org/pypi/pyserial/2.7

	4. Create a "dev.py" file in the dashboard folder with these lines of code:

#----start-----#
class environment:
	# set to "True" whenever you need to work with the GUI and random numbers should be generated
	# set to "False" whenever the can bus should be read
	guiDev = True

	# set interface to listen to for can messages
	# 	vcan0: 	used for dev on linux and for development
	#		can0:		used for actual hardware messages and the production configuration
	bus = "vcan0"
#------end------#

		This file only tells the program to generate random values instead of reading values from a can bus.

	5. Now start editing gauges.py and widgetComiler.py to create custom gauges