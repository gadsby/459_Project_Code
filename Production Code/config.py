
# USER SPECIFIC - OLIVER
comPorts = ['/dev/cu.usbmodem1411', '/dev/cu.usbmodem1421']
dataFolder = '/Users/olivergadsby/Desktop/ENPH 459/459_Project_Code/Results'
torqueListPath = '/Users/olivergadsby/Desktop/outputControllers.csv'

## USER SPECIFIC - RASPBERRY PI
#comPorts = ['/dev/cu.usbmodem1411', '/dev/cu.usbmodem1421']
#dataFolder = '/home/pi/GitStuff/459_Project_Code/Results'
#torqueListPath = '/home/pi/GitStuff/459_Project_Code/Production Code/dummy_outputControllers.csv' # only one, need to modify file structure to accomodate more





######################### Interfacing Parameters #########################

# MOTOR PARAMS
address = 0x80
baudRate = 115200
pulsePerRotation = 768 	#12*64

# ADC PARAMS
potentiometer_adc = 0
SPICLK  = 0x12 #18
SPIMOSI = 0x18 #24
SPIMISO = 0x17 #23
SPICS   = 0x19 #25
maxADC  = 1024 #2^10




######################### Metadata Parameters #########################

metadataNames = ['torqueListPath', 'shankLength', 'thighLength',
	'trunkLength', 'shankMass', 'thighMass', 'trunkMass', 'initialAngle_Knee',
	'initialAngle_Hip', 'calibratedValues']	




######################### Motor Parameters #########################

torque_motorConstant = 13.4e-3 					#torque constant
angVel_motorConstant = 1.4660765716752367e-4 	#angVel constant, 1.4e-3 * 2*pi/60
armRes_motorConstant = 1.9 						#armature resistance




######################### Physical System Parameters #########################

# PHYSICAL LENGTHS
shankLength = 1
thighLength = 1
trunkLength = 1

# PHYSICAL MASSES
shankMass = 1
thighMass = 1
trunkMass = 1

# INITIAL ANGLES
initialAngle_Knee = 0
initialAngle_Hip = 0




######################### Modified by Program #########################

calibratedValues = [] # knee, hip, heel, saves as encoder value
calibrated = False
torqueManager = []
torqueListGenerated = False




######################### Physical System Parameters (Raw) #########################

#L = 1.60  # Total height of the human subject
#M = 53.7  # Total mass of the human subject
#L0 = 0.039*L # foot height
#L1 = (0.285-0.039)*L # Shank length
#L2 = (0.53-0.285)*L # Thigh length
#L3 = (0.818-0.53)*L # Trunk length
#L4 = (1-0.818)*L # Head and neck length
#rCOM_1 = 0.394 # Distal distance of center of mass of the foot and shank segment given as a percent of shank length
#rCOM_2 = 0.567 # Distal distance of center of mass of the thigh segment given as a percent of thigh length
#rCOM_3 = 0.626 # Proximal distance of center of mass of the HAT (Head, Arms, Trunk) segment given as a percent of trunk length
#rG_1 = 0.572 # Distal radius of gyration of the foot and shank segment given as a percent of shank length
#rG_2 = 0.653 # Distal radius of gyration of the thigh segment given as a percent of thigh length
#rG_3 = 0.798 # Proximal radius of gyration of HAT segment given as percent of trunk length
#M1 = 0.061*M # Foot and shank mass
#M2 = 0.1*M # Thigh mass
#M3 = 0.5*(0.678*M) # Half the mass of the HAT segment
#g = 9.8 # gravitational acceleration

#teta_01 = pi/2+5*pi/180; # Ankle angle - Initial condition
#teta_02 = 40*pi/180; # Knee angle - Initial condition
#teta_03 = -40*pi/180; # Hip angle - Initial condition
#dteta_01 = 0 ; # Ankle angular velocity - Initial condition
#dteta_02 = 0; # Knee angular velocity - Initial condition
#dteta_03 = 0; # Hip angular velocity - Initial condition



