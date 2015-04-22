#Dash Runner Class

## Instance Methods

####____init____(self, parent)

sets up tkinter environment to the parent application
sets up the background color, width, height
sets up can store

- __randomly__ generated values
- __can__ read values

read in can bus ids to canStore

handles a file not found exception if initialization xml is not setup properly

calls all the widgets from widget compiler and calls __create__ on each gauge

sets up callback to update can every 10 milliseconds

####__reset__(self)

void is not implemented and not used

####__updateCan__(self)

call for store to update from can bus

self call to update screen

####__alert__(self, label, message)
	
takes main label and message to throw to the screen

wipes the screen of all gauges and only shows the alert message to the driver

#Dash Exceptions

##Missing ID Exception

Inherits: Exception

Holds the wrong id that threw exception.
Thrown when reading xml has an unidentified id.

## Unsafe Operation Exception

Thrown if any parameter is operating outside the safe range

Holds warning message and the unsafe frame struct

# Data store

## Can Listener

sub process that constantly updates can data and the can data packet

listens for pipe query to send updated data packet back to the GUI program

## CanStore

####____init____(self)

initializes and starts can listening sub process

Sets up the correct CAN bus network to listen to

####__ loadConfigXml__(self, xmlPath)

reads in config xml file that defines all the frame configuration data. 

All data is read into a canFrame struct

####__get__(self, frameId)

if the frame id is a valid frame in the can store's dictionary than return the can frame

####__getPack__(self, packIds)

consolidate all the data frames that correlate with the given packIds.

returns an array of canFrame structs in the same order as the given packIds

####__update__(self)

polls canListern sub process to update all the can frames in the data store

## RandomStore(CanStore)

inherits all the methods of canStore and will override all methods that directly deal with the can bus

####____init____(self)

Only __creates__ a frame dictionary

####__update__(self)

For every frame in the frame dictionary, generate a random value within it's min and max range, if that particular frame has a defined min and max

##canFrame class

struct class that holds a all the data for a parameter that is sent over the can network. Mirrors the structure of the xml configuration file

###instance variables:
	
- __canId__ (string)
	
	ID that is used on the CAN network

- __parameter__ (string)

	can frame name (i.e. RPM, TPS, coolant temp, battery voltage)

- __length__ (string)

	length of the data packet

- __type__

	data type of the sent data in the can frame (i.e unsigned int, signed int, boolean)

- __data__

	data of the can frame

- __max__

	maximum safe operating range

- __warning__

	warning message that will display when the safe operating range is exceeded

- __min__

	minimum safe operating range

#EnvironmentConfig class

####__instance__ Variables

- __bus__
	
	bus network name. This should be the same name in linux if you run the command:

		ifconfig

- __framesFileDecleration__

	absolute path to the can ids xml configuration file

- __envType__

	environment type. See the environment static enums

####__static__ enums

- __DEV__

	designates a developer environment where both the GUI and ecu can bus simulator is used

- __DASH__

	designates a production GUI environment. This should be used on the beaglebone that shows the dashboard.

- __PUSH__

	designates a production ecu can bus simulator environment. This should be used on the beaglebone that pushes can bus data to for the GUI to read


#Gauge Class

The gauge class is used during rendering to define how information is displayed to the driver. The three methods that are required are an ____init____, __create__, and __updateView__ method

###Gauge abstract class

####__Instance__ Variables

- __dataIds__

	can bus ids that the gauge has subscribed to

- __xloc__

- __yloc__

- __width__

- __height__

####__Instance__ Methods

- __subscribe__(self, canIds*)

	add all the canIds that the gauge needs to listen to

- __getSubscriptions__()

	return all the subscription ids that the gauge has subscribed to

###TextGauge(Gauge)

Inherits: Gauge

Can display any id or parameter, with no limit on the number of ids that can show up. If there are more than one id that is subscribed to the next id is rendered underneath the previous one.  

####__Instance__ Variables

- __fontSize__

	the font size when text is displayed to the screen

- __fontColor__

####__Instance__ Methods

- ____init____(self, x, y, *subscriptions, fontSize=12, font="Times", fontcolor="black")

- __create__(self, canvas)

	sets the tkinter canvas to draw to

	sets up the initial drawing of the text gauge

- __updateView__(self, dataPack)

	redraws the gauge with the updated dataPack

	dataPack should be an dictionary of <id, values>

- __renderText__(self, dataPack)

	for every id that has been subscribed to, renders the title and the value to the screen

###Circular Gauge(Gauge)

Inherits: Gauge

Can only display one id or parameter that has a defined min and max value in the canids.xml file. 

####__Instance__ Variables

- __startAngle__

	angle that the gauge 0 value should start at relative the -__y__ vector

- __color__

	color of the filled in gauge

- __font__

	fontStyle that is used for the rendered text. Reference tkinter for available fonts

- __fontColor__

####__Instance__ Methods

- ____init____(self, x, y, width, height, subscription, startAngle=0, color="black", font="Times", fontcolor = "black")

- __create__(self, canvas)

- __updateView__(self, dataPack)


###BarGauge(Gauge)

Inherits: Gauge

Renders any number of ids or parameters that have a defined minimum and maximum value in the canids.xml file. For multiple ids that have been subscribed to, the extra ids are rendered next to the first id. The first gauge is where the xloc and yloc point to and then the rest of the gauges are rendered next to it horizontally or vertically depending on the initialization of the gauge.

####__Instance__ Variables

- __fontColor__

- __orientation__ = HORIZONTAL,	VERTICAL

- __padding__
	
	sets the gap between multiple gauges

- __color__

	bar color

- __fontcolor__

####__Static__ Enums

- __HORIZONTAL__ - sets gauge to be rendered horizontally with text on left, bar on right, and multiple gauges rendered underneath first gauge.

- __VERTICAL__ - sets gauge to be rendered vertically with text at bottom, bar on top, and multiple gauges rendered to the right of the first gauge.

####__Instance__ Methods

- ____init____(self, x, y, width, height, *subscriptions, orientation=HORIZONTAL, padding=5, color="black", font="Times", fontcolor="black")

- __create__(self, canvas)

	sets the tkinter canvas to render to

- __updateView__(self, dataPack)

	updates the display

###warningGauge(gauge)

####__Instance__ Variables

- __fontColor__

- __oncolor__

	color of the warning light when it is turned on

- __ofcolor__

	color of the warning light when it is turned off

- __fontcolor__

- __displayText__

	text to display when the warning light is turned on

- font

	font of the displayed text

####__Instance Methods__
- ____init____(self, x, y, width, height, *subscriptions, fontSize=12, offcolor="black", oncolor="black", displayText="warning", font="Times", fontcolor="black", warningColor="red")

- __create__(self, canvas)

	sets the tkinter canvas to render to

- __updateView__(self, dataPack)

	updates the display

#Helper Methods

####__compileGauges__()

Where all the gauges are added to the gauge array and were all the gauges are initialized. The Gauge array is passed back to the main runner where all the declared gauges are rendered to the screen.

To add a gauge to the gauge array:
	
	gauges.append({guaugeType})