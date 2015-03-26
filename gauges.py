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
	def __init__(self):
		# subscribe is how you say "this gauge is going to need access to the rpm and barometer data" where rpm data is correlated to the 0CFFF048 id from the xml file
		self.subscribe("0CFFF048") # rpm
		self.subscribe("0CFFF148") # Barometer
		self.subscribe("0CFFF050") # TPS
		self.subscribe("0CFFF150") # map


	# create will be run once and it is in charge of setting up the initial screen
	# it would be best to have everything rendered at relative x and y coordinates from the self.xloc and self.yloc
	# 	that way it is much easier to move everything around when we are getting the final look
	def create(self, canvas):
		self.canvas = canvas
		self.renderText()

	# is called every time new data appears over the can bus
	# 	the best way that I found to refresh a gauge is to use the ids thrown back after saved from the the create_[line, text, etc] and delete the element
	# 	with that out of the way you can redraw the gauge with updated values
	# 
	# 	It is also easiest to have separate helper function (renderText in this case) that is in charge of drawing the gauge given different parameters
	# 	This way there is any code duplication and everything is easier to manage. In general, if you ever use copy/paste your doing something wrong that will end up 
	# 	making things harder for you. If you have any questions about how to structure some code just talk to me.
	def updateView(self, dataPack):
		self.canvas.delete(self.rpmReference) # deletes the rpm text using the rpmReference id that is saved as a class variable
		self.canvas.delete(self.barometerId)	# deletes the barometer text using the barometerId that is saved as a class variable
		self.canvas.delete(self.tpsId) 				# deletes the tps text using the tpsId that is saved a class variable
		self.canvas.delete(self.mapId)				# deletes the map text using the tpsId that is saved a class variable
		self.renderText(rpm=dataPack[0].data, barometer=dataPack[1].data, tps=dataPack[2].data, map=dataPack[3].data)

	# this is the crap part lots of copy code... #itworks #doAsIsayAndNotAsIdo #hashTagsInCommentsWTF? #ImTired
	def renderText(self, rpm=0, barometer=0, tps=0, map=0):
		# saves a reference to the created text element in rpmReference
		self.rpmReference = self.canvas.create_text(self.xloc, self.yloc,anchor="nw", font=(120), text="RPM: {0}".format(rpm)) # creates the text on the screen

		(rpmx1, rpmy1, rpmx2, rpmy2) = self.canvas.bbox(self.rpmReference) #returns the bounding box of the rpm text box (upper left (x,y), lower right (x,y))
		rpmwidth = rpmx2 - rpmx1
		rpmHeight = rpmy2 - rpmy1

		# saves a reference to the barometer text element. xloc and yloc are NOT hard coded. Hard coding things is bad.
		self.barometerId = self.canvas.create_text(self.xloc, self.yloc + rpmHeight, anchor="nw", font=(120), text="Barometer: {0}".format(barometer)) # creates the barometer text on the screen
		
		(barx1, bary1, barx2, bary2) = self.canvas.bbox(self.barometerId) #returns the bounding box of the rpm text box (upper left (x,y), lower right (x,y))
		barwidth = barx2 - barx1
		barHeight = bary2 - bary1

		# saves a reference to the tps text element. xloc and yloc are NOT hard coded. Hard coding things is bad.
		self.tpsId = self.canvas.create_text(self.xloc, self.yloc + rpmHeight + barHeight, anchor="nw", font=(120), text="TPS: {0}".format(tps)) # creates the barometer text on the screen

		(tpsx1, tpsy1, tpsx2, tpsy2) = self.canvas.bbox(self.tpsId) #returns the bounding box of the rpm text box (upper left (x,y), lower right (x,y))
		tpswidth = tpsx2 - tpsx1
		tpsHeight = tpsy2 - tpsy1

		# saves a reference to the tps text element. xloc and yloc are NOT hard coded. Hard coding things is bad.
		self.mapId = self.canvas.create_text(self.xloc, self.yloc + rpmHeight + barHeight + tpsHeight, anchor="nw", font=(120), text="map: {0}".format(map)) # creates the barometer text on the screen

# CODE EVERYTHING UNDER HERE