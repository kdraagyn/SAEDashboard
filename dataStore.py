import xml.etree.cElementTree as xmlreader
from dashExceptions import *
import can
from can.interfaces.interface import Bus

class canStore(object):
	can_interface = 'vcan0' # sets up the can network it will listen to
	filters = []

	"""data structure and manager for all data in the program"""
	def __init__(self):
		
		super(canStore, self).__init__()
		self.frameDictionary = {}


	def loadConfigXml(self, xmlPath):
		ids = xmlreader.parse(xmlPath)
		for xmlframe in ids.findall("frame"):

			frame = canFrame()
			frame.canId = xmlframe.findtext("canId")
			frame.parameter = xmlframe.findtext("parameter")
			frame.length = int(xmlframe.findtext("length"))
			frame.type = xmlframe.findtext("type")
			if(xmlframe.findtext("max") != None):
				frame.max = int(xmlframe.findtext("max"))
			if(xmlframe.findtext("warning") != None):
				frame.warning = xmlframe.findtext("warning")

			self.filters.append({'can_id':int(frame.canId,16), 'can_mask':0x1fffffff})
			self.frameDictionary[frame.canId] = frame

		# set up can bus interface
		self.bus = Bus(self.can_interface)

	def get(self, frameId):
		if(frameId not in self.frameDictionary):
			raise missingIdException(frameId)
		return self.frameDictionary[frameId]

	def getPack(self, packIds):
		pack = []
		for frameId in packIds:
			pack.append(self.get(frameId))
		return pack

	def update(self):
		for frame in self.frameDictionary:
			msg = self.bus.recv()

			ident = hex(msg.arbitration_id).replace('0x','').upper()
			if(len(ident) == 7):
				ident = '0' + ident
			if(ident in self.frameDictionary):
				self.frameDictionary[ident].data = int.from_bytes(msg.data, byteorder='little', signed=True)

				if(self.frameDictionary[ident].max != None):
					if(self.frameDictionary[ident].data > self.frameDictionary[ident].max):
						raise unsafeOperationException(self.frameDictionary[ident])


class canFrame(object):
	"""PE3 ECU can frame struct"""
	def __init__(self):
		super(canFrame, self).__init__()
		self.canId = ""
		self.parameter = ""
		self.length = 0
		self.type = ""
		self.data = 200
		self.max = None
		self.warning = None