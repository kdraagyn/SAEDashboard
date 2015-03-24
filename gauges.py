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

	def subscribe(self, *canIds):
		for canId in canIds:
			if(canId not in self.dataIds):
				self.dataIds.append(canId)

	def getSubscriptions(self):
		return self.dataIds
#
# Alright you're past the danger zone. Just add your gauge class down below
# 

class textGauge(gauge):
	def __init__(self):
		self.subscribe("0CFFF048") # rpm
		self.subscribe("0CFFF148") # Barometer

	def create(self, canvas):
		self.canvas = canvas
		self.rpmId = self.canvas.create_text(0,0,anchor="nw", text="Rpm:")
		self.barometerId = self.canvas.create_text(0,20, anchor="nw", text="barometer:")

	def updateView(self, dataPack):
		self.canvas.delete(self.rpmId)
		self.canvas.delete(self.barometerId)
		self.rpmId = self.canvas.create_text(0,0,anchor="nw", text="RPM:\t{0}".format(dataPack[0].data))
		self.barometerId = self.canvas.create_text(0,20, anchor="nw", text="Barometer:\t{0}".format(dataPack[1].data))
