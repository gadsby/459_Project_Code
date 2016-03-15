# USER SPECIFIC - OLIVER
comPorts = ['/dev/cu.usbmodem1411', '/dev/cu.usbmodem1421']
dataFolder = '/Users/olivergadsby/Desktop/ENPH 459/459_Project_Code/Results'
torqueListPath = '/Users/olivergadsby/Desktop/MATLAB_code.csv' # only one, need to modify file structure to accomodate more



# FIXED
address = 0x80
baudRate = 115200
gpioPin = 18
pulsePerRotation = 768

# TUNEABLE
kp = {'knee' : 1, 'hip' : 1}
kd = {'knee' : 0, 'hip' : 0}
ki = {'knee' : 0, 'hip' : 0}


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



# PROGRAM MODIFIABLE; THESE ARE DEFAULTS
calibratedValues = [] # knee, hip, heel
calibrated = False
torqueManager = []
torqueListGenerated = False

