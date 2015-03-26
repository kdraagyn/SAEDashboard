import xml.etree.cElementTree as xmlreader
from dashExceptions import *
import can
from can.interfaces.interface import Bus
from multiprocessing import Process, Pipe

# have to do fancy things with multiprocessing
# hopefully this performs well on the beaglebone..
def canListener(pipe):
	data = {}
	bus = Bus('vcan0')
	while 1:
		frame = bus.recv(timeout=0.005)
		data[hex(frame.arbitration_id)] = frame.data

		if(pipe.poll(timeout=0)):
			# flush out the pipe from any flags for writing
			while pipe.poll(timeout=0):
				pipe.recv()
			pipe.send(data)
	pipe.close()
	return # execution really should get here

class canStore(object):
	can_interface = 'vcan0' # sets up the can network it will listen to
	filters = []

	"""data structure and manager for all data in the program"""
	def __init__(self):
		
		super(canStore, self).__init__()
		self.frameDictionary = {}

		# setup worker multiprocessing to listen to the can bus
		self.parent, self.child = Pipe()
		self.canWorker = Process(target=canListener, args=(self.child,))
		self.canWorker.start()


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
		# hand shake with canListener process to get data for all changing values
		self.parent.send(True)
		data = self.parent.recv()

		for msg in data:
			ident = msg.replace('0x','').upper()
			if(len(ident) == 7):
				ident = '0' + ident
			if(ident in self.frameDictionary):
				self.frameDictionary[ident].data = int.from_bytes(data[msg], byteorder='little', signed=True)
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