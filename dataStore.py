import xml.etree.cElementTree as xmlreader
from dashExceptions import *

class canStore(object):
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
			print(frame.max)

			self.frameDictionary[frame.canId] = frame

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
			# TODO update through can bus
			self.frameDictionary[frame].data += 50
			if(self.frameDictionary[frame].max != None):
				if(self.frameDictionary[frame].data > self.frameDictionary[frame].max):
					raise unsafeOperationException(self.frameDictionary[frame])


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