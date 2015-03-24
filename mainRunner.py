import tkinter as tk
from tkinter import *
from dataStore import canStore
from gauges import *
from dashExceptions import *
from widgetCompiler import * 

configName = "ids.xml"
height = 720
width = 1280

"""
	dashRunner is in charge of:
		pulling new values off of the can bus
		plugging in the values to the screen 
		managing the screen

	Initializes 
		tkinter size and variables
		can bus ids from config file
"""
class dashRunner(tk.Tk):
	widgets = [] # used to store all the widgets that are displayed on the screen

	def __init__(self, parent):
		# setup tkinter
		tk.Tk.__init__(self, parent)
		self.parent = parent # even though dashRunner is the parent of all gui elements
		self.canvas = tk.Canvas(self, height=height, width=width)
		self.canvas.configure(background="white")
		self.canvas.grid()

		self.widgets = compileGauges() # pulls from widgetCompiler where all the gauges are declared

		# injects the canvas object so the widgets can be drawn
		for widget in self.widgets:
			widget.create(self.canvas)

		# sets up for can bus to update every 10 milliseconds. So a refresh rate of at least 100 Hz
		self.after(10, self.updateCAN)

		# figure out all indexes and frames to read
		# load in the xml with all the can ids and can frame configuration data
		self.store = canStore()
		
		try:
			self.store.loadConfigXml(configName)
		except FileNotFoundError:
			self.alert("Initialization Error!", "FileNotFoundError: configuration name \"" + configName +"\" is incorrect")

		# TODO: plug in the can bus


	def reset(self):
		# reset everything so init is called again in case an issue arises
		pass

	def updateCAN(self):
		# Pull values from the can bus for all the gauges and update all of their information
		self.store.update()
		self.updateScreen()
		self.after(5, self.updateCAN)
		pass

	def updateScreen(self):
		# update screen with the proper values from can bus
		for widget in self.widgets:
			try:
				widgetPack = self.store.getPack(widget.getSubscriptions())
				widget.updateView(widgetPack)
			except missingIdException as miss:
				self.alert("bad data store ID\n\t", 
					miss.id + " is not contained in the data store\n" + 
					"bad subscriptions in the widget:" + type(widget).__name__)

	# method to take everything off the screen and display a warning message
	def alert(self, label, message):
		# remove previously viewable widgets
		self.canvas.delete("all")

		xloc = self.canvas.winfo_reqwidth() * (1 / 2)
		xwidth = self.canvas.winfo_reqwidth() * (5 / 6)
		yloc = self.canvas.winfo_reqheight() * (3 / 11)
		messageWidth = xwidth * (3 / 5)

		self.canvas.configure(background="red")
		labelref = self.canvas.create_text(xloc, yloc, anchor="n", width=xwidth, text=label, font=("Helvetica", 72, "bold"))

		(labelx1, labely1, labelx2, labely2) = self.canvas.bbox(labelref)

		self.canvas.create_text(xloc, yloc + (labely2 - labely1) + 20, text=message, font=("Helvetica", 16))
		Label(self, text=message, fg="black")

# Start Application
if __name__ == "__main__":
	app = dashRunner(None)
	app.title("Dashboard")
	app.mainloop()