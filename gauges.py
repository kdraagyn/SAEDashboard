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
class textGauge(gauge): # the class must inherit (i.e the "gauge" within the parentheses) from the main gauge class

	# variables you can use from the gauge class:
	# 	xloc:
	# 	yloc:
	# 	width:
	# 	height:

	# init will run when you first add it to the widget compiler
	# 	this is were you setup which ids you will use
	# 	ids are the same ids as in the ids.xml and they correlate with a piece of data. This also can be seen from the .xml
	def __init__(self):
		# subscribe is how you say "this gauge is going to need access to the rpm and barometer data" where rpm data is correlated to the 0CFFF048 id from the xml file
		self.subscribe("0CFFF048") # rpm
		self.subscribe("0CFFF148") # Barometer


	# create will be run once and it is in charge of setting up the initial screen
	# it would be best to have everything rendered at relative x and y coordinates from the self.xloc and self.yloc
	# 	that way it is much easier to move everything around when we are getting the final look
	def create(self, canvas):
		self.canvas = canvas
		self.renderText()

	def updateView(self, dataPack):
		self.canvas.delete(self.rpmReferance)
		self.canvas.delete(self.barometerId)
		self.renderText(rpm=dataPack[0].data, barometer=dataPack[1].data)

	def renderText(self, rpm=0, barometer=0):
		self.rpmReferance = self.canvas.create_text(self.xloc, self.yloc,anchor="nw", text="RPM: {0}".format(rpm))

		(rpmx1, rpmy1, rpmx2, rpmy2) = self.canvas.bbox(self.rpmReferance) 
		width = rpmx2 - rpmx1
		rpmHeight = rpmy2 - rpmy1

		self.barometerId = self.canvas.create_text(self.xloc, self.yloc + rpmHeight, anchor="nw", text="Barometer: {0}".format(barometer))