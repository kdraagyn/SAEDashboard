import tkinter as tk
from dataStore import canStore

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
	def __init__(self):
		super(dashRunner, self).__init__()
		self.after(10, self.updateCAN)

		# figure out all indexes and frames to read
		# load in the xml with all the can ids and can frame configuration data
		self.store = canStore()
		self.store.loadConfigXml("ids.xml")
		# TODO: plug in the can bus

	def reset(self):
		# reset everything so init is called again in case an issue arises
		pass
	def updateCAN(self):
		# Pull values from the can bus for all the gauges and update all of their information
		# print("updating CAN")
		self.after(10, self.updateCAN)
		pass
	def updateScreen(self):
		# update screen with the proper values from can bus
		pass

if __name__ == "__main__":
	app = dashRunner()
	app.title("Dashboard")
	app.mainloop()