import xml.etree.cElementTree as xmlreader

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

			self.frameDictionary[frame.canId] = frame
			print(len(self.frameDictionary))

	def get(id):
		return self.frameDictionary[id]

	def updateData():
		for frame in self.frameDictionary:
			# update through can buss
			pass


class canFrame(object):
	"""PE3 ECU can frame struct"""
	def __init__(self):
		super(canFrame, self).__init__()
		self.canId = ""
		self.parameter = ""
		self.length = 0
		self.type = ""
		self.data = 0