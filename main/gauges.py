import tkinter as tk
from tkinter import *
# 
# Base class for every gauge. DO NOT EDIT THIS CLASS. If you edit anything in this
# 	class all the views will break so just steer clear :)
# 
# edit it and chuck norris will press ctrl-z so hard that it will undo your whole life
"""base class of all gauges added to dashboard"""
class gauge:
	def __init__(self):
		self.__dataIds = []
		self.xloc = 0
		self.yloc = 0
		self.width = 0
		self.height = 0

	def subscribe(self, *canIds):
		for canId in canIds:
			if(canId not in self.__dataIds):
				self.__dataIds.append(canId)

	def getSubscriptions(self):
		return self.__dataIds

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
	def __init__(self, x, y, *subscriptions):
		super(textGauge, self).__init__()
		# set gauge view x and y location
		self.xloc = x
		self.yloc = y

		# subscribe is how you say "this gauge is going to need access to the rpm and barometer data" where rpm data is correlated to the 0CFFF048 id from the xml file
		for subscription in subscriptions:
			self.subscribe(subscription)

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
		# for pack in dataPack:
		# 	if(pack.canId in self.elementRef): self.canvas.delete(self.elementRef[pack.canId])

		self.renderText(dataPack)

	# render all the dataPack on screen
	def renderText(self, dataPack):
		pasty = 0

		# loop through data pack and create all the text elements
		for pack in dataPack:
			# saves reference to the created text element in refDictionary
			self.elementRef[pack.canId] = self.canvas.create_text(self.xloc, self.yloc + pasty, anchor="e", font=("Times", 12, ), text="{0}: {1}".format(pack.parameter, pack.data))

			(pastx1, pasty1, pastx2, pasty2) = self.canvas.bbox(self.elementRef[pack.canId])
			pastHeight = pasty2 - pasty1
			pasty += pastHeight

class circularGauge(gauge):
	def __init__(self, x, y, width, height, *subscriptions, startAngle=0):
		super(circularGauge, self).__init__()
		for subscription in subscriptions:
			self.subscribe(subscription)

		self.xloc = x
		self.yloc = y
		self.width = width
		self.height = height
		self.startAngle = startAngle
		self.elementRef = []

	def create(self, canvas):
		self.canvas = canvas

	def updateView(self, dataPack):
		for pack in dataPack:
			startAngle = -180 + self.startAngle
			endAngle = 180 - self.startAngle

			# Main display circular gauge
			self.elementRef.append(self.canvas.create_arc(self.xloc, 
				self.yloc, 
				self.xloc + self.width, 
				self.yloc + self.height, 
				style=tk.PIESLICE, 
				fill="green", 
				start=-180 + self.startAngle,
				extent=-(pack.data / pack.max * (endAngle - startAngle))))

			# "eraser" gauge
			eraserbuffer = self.width / 10
			self.elementRef.append(self.canvas.create_arc(self.xloc + eraserbuffer, 
				self.yloc + eraserbuffer, 
				self.xloc + self.width - eraserbuffer, 
				self.yloc + self.height - eraserbuffer, 
				style=tk.PIESLICE, 
				fill=self.canvas["background"], 
				start= -self.startAngle,
				extent= endAngle - startAngle - 30,
				outline=self.canvas["background"]))

			self.elementRef.append(self.canvas.create_text(self.xloc + self.width / 2, self.yloc + self.height / 3, 
				font=("Helvetica", int(150 * self.width / int(self.canvas["width"])), "bold"), 
				text="{0}".format(pack.data).upper()))

			self.elementRef.append(self.canvas.create_text(self.xloc + self.width / 2, self.yloc + 4 * self.height / 9,
				font=("Helvetica", int(75 * self.width / int(self.canvas["width"])), "bold"),
				text="{0}".format(pack.parameter).upper()))

# CODE EVERYTHING UNDER HERE