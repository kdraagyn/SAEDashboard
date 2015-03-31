class config(object):
	"""class that holds main program configuration data."""
	configName = "canids.xml"
	height = 720
	width = 1280

	# set to "True" whenever you need to work with the GUI, False whenever the can 
	# 	bus should be used
	guiDev = True