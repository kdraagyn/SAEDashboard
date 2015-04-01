import tkinter as tk
from tkinter import *

# 
# Base class for every gauge. DO NOT EDIT THIS CLASS. If you edit anything in this
# 	class all the views will break so just steer clear :)
# 
# edit it and chuck norris will press ctrl-z so hard that it will undo your whole life
"""base class of all gauges added to dashboard"""
class gauge():
	dataIds = []
	xloc = 0
	yloc = 0
	width = 0
	height = 0

	def setLocation(xloc=0, yloc=0, width=0, height=0):
		self.xloc = xloc
		self.yloc = yloc
		self.width = width
		self.height = height

	def subscribe(self, *canIds):
		for canId in canIds:
			if(canId not in self.dataIds):
				self.dataIds.append(canId)

	def getSubscriptions(self):
		return self.dataIds
#
# Alright you're past the danger zone. Just add your gauge class down below
# 

# Here is an example gauge class that doesn't do anything really except a few text fields
# This is not the ideal gauge. This is me programming at 6 in the morning and just wanting to get something working. yes.
class textGauge(gauge): # the class must inherit (i.e the "gauge" within the parentheses) from the main gauge class

	# variables you can use from the gauge class:
	# 	xloc:
	# 	yloc:
	# 	width:
	# 	height:

	# init will run when you first add it to the widget compiler
	# 	this is were you setup which ids you will use
	# 	ids are the same ids as in the ids.xml and they correlate with a piece of data. This also can be seen from the .xml
	def __init__(self, x, y):
		# set gauge view x and y location
		self.xloc = x
		self.yloc = y

		# subscribe is how you say "this gauge is going to need access to the rpm and barometer data" where rpm data is correlated to the 0CFFF048 id from the xml file
		self.subscribe("0CFFF048") # rpm
		self.subscribe("0CFFF148") # Barometer
		self.subscribe("0CFFF050") # TPS
		self.subscribe("0CFFF150") # map
		self.subscribe("0CFFF052") # Fuel Open Time
		self.subscribe("0CFFF054") # Ignition Angle
		self.subscribe("0CFFF152") # Lambda
		self.subscribe("0CFFF154") # Pressure Type
		self.subscribe("0CFFF248") # Analog Input 1
		self.subscribe("0CFFF250") # Analog Input 2
		self.subscribe("0CFFF252") # Analog Input 3
		self.subscribe("0CFFF254") # Analog Input 4
		self.subscribe("0CFFF348") # Analog Input 5
		self.subscribe("0CFFF350") # Analog Input 6
		self.subscribe("0CFFF352") # Analog Input 7
		self.subscribe("0CFFF354") # Analog Input 8
		self.subscribe("0CFFF448") # Frequency 1
		self.subscribe("0CFFF450") # Frequency 2
		self.subscribe("0CFFF452") # Frequency 3
		self.subscribe("0CFFF454") # Frequency 4
		self.subscribe("0CFFF548") # Battery Voltage
		self.subscribe("0CFFF550") # Air Temp
		self.subscribe("0CFFF552") # Coolant Temp
		self.subscribe("0CFFF554") # Temp Type
		self.subscribe("0CFFF648") # Analog Input 5 - Thermistor
		self.subscribe("0CFFF650") # Analog Input 6 - Thermistor
		self.subscribe("0CFFF652") # Version Major
		self.subscribe("0CFFF654") # Version Minor
		self.subscribe("0CFFF656") # Version Build
		self.subscribe("0CFFF658") # TBD

		self.elementRef = {};


	# create will be run once and it is in charge of setting up the initial screen
	# it would be best to have everything rendered at relative x and y coordinates from the self.xloc and self.yloc
	# 	that way it is much easier to move everything around when we are getting the final look
	def create(self, canvas):
		self.canvas = canvas

	# is called every time new data appears over the can bus
	# 	the best way that I found to refresh a gauge is to use the ids thrown back after saved from the the create_[line, text, etc] and delete the element
	# 	with that out of the way you can redraw the gauge with updated values
	# 
	# 	It is also easiest to have separate helper function (renderText in this case) that is in charge of drawing the gauge given different parameters
	# 	This way there is any code duplication and everything is easier to manage. In general, if you ever use copy/paste your doing something wrong that will end up 
	# 	making things harder for you. If you have any questions about how to structure some code just talk to me.
	def updateView(self, dataPack):
		for pack in dataPack:
			if(pack.canId in self.elementRef): self.canvas.delete(self.elementRef[pack.canId])

		self.renderText(dataPack)

	# this is the crap part lots of copy code... #itworks #doAsIsayAndNotAsIdo #hashTagsInCommentsWTF? #ImTired
	def renderText(self, dataPack):
		pasty = 0

		for pack in dataPack:
			# saves reference to the created text element in refDictionary
			self.elementRef[pack.canId] = self.canvas.create_text(self.xloc, self.yloc + pasty, anchor="nw", font=(120), text="{0}: {1}".format(pack.parameter, pack.data))

			(pastx1, pasty1, pastx2, pasty2) = self.canvas.bbox(self.elementRef[pack.canId])

			pastWidth = pastx2 - pastx1
			pastHeight = pasty2 - pasty1

			pasty += pastHeight

		# saves a reference to the created text element in rpmReference
		# self.rpmReference = self.canvas.create_text(self.xloc, self.yloc,anchor="nw", font=(120), text="RPM: {0}".format(rpm)) # creates the text on the screen

# CODE EVERYTHING UNDER HERE