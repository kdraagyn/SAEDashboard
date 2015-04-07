from main.environmentConfig import *
import os

def startDash():
	os.system("cd main; export DISPLAY=:0; lxterminal -e python3.4 mainRunner.py &")

def startPush():
	os.system("export DISPLAY=:0; lxterminal -e python3.4 -m tools.pushCan &")

# Start Application
if __name__ == "__main__":
	# kill all running python processes except this one ;)
	f = os.popen("ps -aux | grep python")
	processes = f.read()
	for process in processes.split("\n"):
		processIds = process.split()
		if(len(processIds) > 0):
			if(processIds[-1] != __file__):
				os.system("kill " + processIds[1])

	if(environment.envType == environment.DEV):
		startDash()
		startPush()
	elif(environment.envType == environment.DASH):
		startDash()
	elif(environment.envType == environment.PUSH):
		startPush()