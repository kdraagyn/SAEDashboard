import can
from can.interfaces.interface import Bus
import struct
import sys
import re

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

can_interface = 'vcan0'
range_reg = "([0-9]+):([0-9]+)"
range_pattern = re.compile(range_reg)

def pushCan(canId, data):
	bus = Bus(channel=can_interface)
	msg = can.Message(arbitration_id=canId, data=(data).to_bytes(4, byteorder='little'), extended_id=True)
	bus.send(msg);

while True:
	command = input("")
	commands = command.split(" ")
	if((len(sys.argv) - 1) % 2 == 0):
		for x in range(0,len(commands),2):
			parameter = commands[x]
			if(parameter in param2id):
				canId = param2id[parameter]

				value = commands[x+1]
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

	else:
		print("not enough pairs")

