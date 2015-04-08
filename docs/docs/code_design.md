#Dash Runner Class

####__init__(self, parent)

	sets up tkinter environment to the parent application
	sets up the background color, width, height
	sets up can store

	- randomly generated values
	- can read values

	read in can bus ids to canStore

	handles a file not found exception if initialization xml is not setup properly

	calls all the widgets from widget compiler and calls create on each gauge

	sets up callback to update can every 10 milliseconds

####reset(self)

	void is not implemented and not used

####updateCan(self)

	call for store to update from can bus

	self call to update screen

####alert(self, label, message)
	
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

####__init__(self)

initializes and starts can listening sub process

Sets up the correct CAN bus network to listen to

#### loadConfigXml(self, xmlPath)

reads in config xml file that defines all the frame configuration data. 

All data is read into a canFrame struct

####get(self, frameId)

if the frame id is a valid frame in the can store's dictionary than return the can frame

####getPack(self, packIds)

consolidate all the data frames that correlate with the given packIds.

returns an array of canFrame structs in the same order as the given packIds

####update(self)

polls canListern sub process to update all the can frames in the data store

## RandomStore(CanStore)

inherits all the methods of canStore and will override all methods that directly deal with the can bus

####__init__(self)

Only creates a frame dictionary

####update(self)

For every frame in the frame dictionary, generate a random value within it's min and max range, if that particular frame has a defined min and max

##canFrame class

struct class that holds a all the data for a parameter that is sent over the can network. Mirrors the structure of the xml configuration file

###instance variables:
	
- canId (string)
	
	ID that is used on the CAN network

- parameter (string)

	can frame name (i.e. RPM, TPS, coolant temp, battery voltage)

- length (string)

	length of the data packet

- type

	data type of the sent data in the can frame (i.e unsigned int, signed int, boolean)

- data

	data of the can frame

- max

	maximum safe operating range

- warning

	warning message that will display when the safe operating range is exceeded

- min

	minimum safe operating range

##EnvironmentConfig class

instance Variables

- bus
	
	bus network name. This should be the same name in linux if you run the command:

		ifconfig

- framesFileDecleration

	absolute path to the can ids xml configuration file

- envType

	environment type. See the environment static enums

static enums

- DEV

	designates a developer environment where both the GUI and ecu can bus simulator is used

- DASH

	designates a production GUI environment. This should be used on the beaglebone that shows the dashboard.

- PUSH

	designates a production ecu can bus simulator environment. This should be used on the beaglebone that pushes can bus data to for the GUI to read