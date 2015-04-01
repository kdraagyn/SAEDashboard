from gauges import *

def compileGauges():
	gauges = [] 

	# declare gauge or view here
	# declaring just means gauges.append("name of gauge class you write"())
	#
	# your code starts here
	gauges.append(textGauge(100, 0))

	# your code stops here

	return gauges