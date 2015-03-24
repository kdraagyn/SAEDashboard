from gauges import *
def compileGauges():
	gauges = []

	# declare gauge or view here
	# declaring just means gauges.append("name of gauge class you write"())
	gauges.append(textGauge()) 


	return gauges