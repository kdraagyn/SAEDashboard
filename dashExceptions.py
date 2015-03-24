class missingIdException(Exception):
	"""no id is found in the data store"""
	def __init__(self, wrongId):
		super(missingIdException, self).__init__()
		self.id = wrongId
		