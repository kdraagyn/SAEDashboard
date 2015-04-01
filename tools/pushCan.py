import can
from can.interfaces.interface import Bus
import struct
import sys
import re
from multiprocessing import Process, Queue
from main.config import *

# command to send all values
# rpm 31000:27000 tps 1:3000 fuel_open_time 1:3000 ignition_angle 1:3000 barometer 1:3000 map 1:3000 lambda 1:3000 pressure_type 1:3000 analog1 1:3000 analog2 1:3000 analog3 1:3000 analog4 1:3000 analog5 1:3000 analog6 1:3000 analog7 1:3000 analog8 1:3000 frequency1 1:3000 frequency2 1:3000 frequency3 1:3000 frequency4 1:3000 battery_voltage 1:15 air_temp 1:3000 coolant_temp 1:3000 temp_type 1:3000 analog5_thermistor 1:3000 analog7_thermistor 1:3000 version_major 1:3000 version_minor 1:3000 version_build 1:3000 tbd 1:3000 


param2id = {
	'rpm': 218099784,
	'tps': 218099792,
	'fuel_open_time': 218099794,
	'ignition_angle': 218099796,
	'barometer': 218100040,
	'map': 218100048,
	'lambda': 218100050,
	'pressure_type': 218100052,
	'analog1': 218100296,
	'analog2': 218100304,
	'analog3': 218100306,
	'analog4': 218100308,
	'analog5': 218100552,
	'analog6': 218100560,
	'analog7': 218100562,
	'analog8': 218100564,
	'frequency1': 218100808,
	'frequency2': 218100816,
	'frequency3': 218100818,
	'frequency4': 218100820,
	'battery_voltage': 218101064,
	'air_temp': 218101072,
	'coolant_temp': 218101074,
	'temp_type': 218101076,
	'analog5_thermistor': 218101320,
	'analog7_thermistor': 218101328,
	'version_major': 218101330,
	'version_minor': 218101332,
	'version_build': 218101334,
	'tbd': 218101336
}

can_interface = config.bus
range_reg = "([0-9]+):([0-9]+)"
range_pattern = re.compile(range_reg)

def pushCan(canId, data):
	bus = Bus(channel=can_interface)
	msg = can.Message(arbitration_id=canId, data=(data).to_bytes(4, byteorder='little'), extended_id=True)
	bus.send(msg);

def canWriter(canId, value):
	# spawned sub process for writing to the can bus
	if(range_pattern.match(value) != None):
		match_object= range_pattern.match(value)
		left = int(match_object.group(1))
		right = int(match_object.group(2))
		if(left < right):
			for x in range(left, right + 1):
				pushCan(canId, x)
		elif(left > right):
			for x in range(0, left - right + 1):
				pushCan(canId, left - x)
		else:
			pushCan(canId, left)
	else:
		pushCan(canId, int(value))
	return True

while True:
	processes = []
	results = Queue()

	command = input("")
	commands = command.split(" ")
	if((len(sys.argv) - 1) % 2 == 0):

		# pull all the commands from the user input
		for x in range(0,len(commands),2):
			parameter = commands[x]

			if(parameter in param2id):
				canId = param2id[parameter]
				value = commands[x+1]
				# spawn sub process
				p = Process(target=canWriter, args=(canId, value))
				p.start()
				processes.append(p)
	else:
		print("not enough pairs")
	
	numberOfProcesses = len(processes)
	for p in processes:
		p.join()
		p.terminate()
