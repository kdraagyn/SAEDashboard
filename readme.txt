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

To see how to declare a new gauge interface look at the gauges.py file. I commented out the textGauge