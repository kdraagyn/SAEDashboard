class missingIdException(Exception):
	"""no id is found in the data store"""
	def __init__(self, wrongId):
		super(missingIdException, self).__init__()
		self.id = wrongId
		
class unsafeOperationException(Exception):
	"""the car has traveled into an unsafe operation region"""
	def __init__(self, unsafeFrame):
		self.warningMsg = "TURN OFF CAR! \n{0}".format(unsafeFrame.warning)
		self.unsafeFrame = unsafeFrame