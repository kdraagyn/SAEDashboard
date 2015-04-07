import os
import subprocess
from subprocess import TimeoutExpired
import re
import main.environmentConfig as env

class beagleUpdater:
	"""handles updating dashboard app on beaglebone"""

	__timeout = 0.5
	__projectDir = "/home/ubuntu/SAEDashboard/"
	__homeDir = "/home/keith"
	__devProjectDir = os.path.abspath(os.path.join(__file__, os.pardir))

	__ignore = [
		".git",
		"__pycache__",
		".gitignore",
		"environmentConfig.py",
		__file__,
		"tests"
	]

	def __init__(self, ipAddress):
		self.ip = ipAddress
		self.failedFiles = []

	def isConnected(self):
		try:
			response = subprocess.call(
				["ping", "-c", "1", "-i", "0.2", self.ip],
				stdout=open(os.devnull, "w"),
				stderr=subprocess.STDOUT,
				timeout=self.__timeout)
			keygen = subprocess.call(
				["ssh", "ubuntu@" + self.ip, "exit"],
				stdout=open(os.devnull, "w"),
				stderr=subprocess.STDOUT)
			if(keygen == 255):
				print("")
				keygen = subprocess.call(
					["ssh-keygen", "-f", self.__homeDir + "/.ssh/known_hosts", "-R", self.ip],
					stderr=subprocess.STDOUT)
		except TimeoutExpired as e:
			return False
		else:
			return response == 0

	def createEnvironment(self):
		# class environment:
		# 	guiDev = False
		# 	bus = "can0"
		# 	framesFileDeclaration = "/home/ubuntu/SAEDashboard/main/canids.xml"
		pass

	def sshCommand(self, subprocessCall):
		try:
			response = subprocess.call(
				subprocessCall,
				stdout=open(os.devnull, "w"),
				stderr=subprocess.STDOUT)
			return True
		except TimeoutExpired as e:
			self.failedFiles.append(path)
			print("FAIL (timeout)")
			return false
	def copyString(self, string, path):
		pass

	def copyFile(self, path):
		print("copying", path, end="", flush=True)
		if(not os.path.isfile(os.path.join(self.__devProjectDir, path))):
			print("...FAIL (unknown file)")	
			return
		if(self.sshCommand(["scp", os.path.join(self.__devProjectDir, path), "ubuntu@" + self.ip + ":" + os.path.join(self.__projectDir, path)])):
			print("")
		else:
			print("FAIL")

	def createDirectory(self, path):
		if(len(path) == 0):
			return
		relPath = path[1:]
		if(not self.sshCommand(["ssh", "ubuntu@" + self.ip, "mkdir", os.path.join(self.__projectDir, relPath)])):
			print("FAIL (can\' create " + path)

	def isSendable(self, path):
		if(path.startswith(self.__devProjectDir)):
			relPath = path.replace(self.__devProjectDir + "/", "")
		else:
			relPath = path
		for ignore in self.__ignore:
			r = re.compile(ignore)
			if(r.search(relPath) != None):
				return False
		return True

	def update(self):
		for dirname, subdirList, fileList in os.walk(self.__devProjectDir):
			if(self.isSendable(dirname)):
				self.createDirectory(dirname.replace(self.__devProjectDir, ""))
				for f in fileList:
					projectPath = os.path.join(dirname, f).replace(self.__devProjectDir + "/", "")
					if(self.isSendable(projectPath)):
						self.copyFile(projectPath)

	def restart(self):
		# call restart python script
		keygen = subprocess.Popen(
				["ssh", "ubuntu@" + self.ip, "cd SAEDashboard/ && python3.4 restart.py"],
				stdout=open(os.devnull, "w"),
				stderr=subprocess.STDOUT)

# Start Application
if __name__ == "__main__":
	# beaglebone ip address
	ip = "192.168.7.2"

	board = beagleUpdater(ip)
	print("Checking for Beaglebone...", end="",flush=True)
	if(board.isConnected()):
		print("OK")
		board.update()
		board.restart()
	else:
		print("FAIL")