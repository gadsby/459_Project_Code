
# LOCAL LIBRARIES
import config
import torqueList

# PYTHON LIBRARIES
import threading
import time
import os
import numpy as np

# ELECTRICAL LIBRARIES
import roboclaw as rc
import RPi.GPIO as GPIO



######################### Setup Electrical Interfacing #########################

motorDetected = False
for comPort in config.comPorts:
    try:
        motorDetected = rc.Open(comPort, config.baudRate)
	break
    except:
        continue
if not motorDetected:
    print('Motor port could not be opened.')
    print('Ports checked:')
    for i in config.comPorts:
    	print('\t'+i)
 	print('Exiting...')
    exit()


# INITIALIZE GPIO PORTS
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(config.SPIMOSI, GPIO.OUT)
GPIO.setup(config.SPIMISO, GPIO.IN)
GPIO.setup(config.SPICLK, GPIO.OUT)
GPIO.setup(config.SPICS, GPIO.OUT)


# put in error detection if ports aren't found




######################### Electrical Interfacing Functions #########################

# COMPLETE
def readPot(adcnum=config.potentiometer_adc, clockpin=config.SPICLK, mosipin=config.SPIMOSI,\
			misopin=config.SPIMISO, cspin=config.SPICS):
    GPIO.output(cspin, True)
    GPIO.output(clockpin, False)
    GPIO.output(cspin, False)
    commandout = (adcnum | 0x18) << 3
    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
    adcout = 0
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if (GPIO.input(misopin)):
            adcout |= 0x1
    GPIO.output(cspin, True)
    return adcout >> 1

## COMPLETE
#def readPot():
#    potVal = 1.5 #readadc()
#    return potVal

# COMPLETE
def readAngles():
	kneeAngle = int(rc.ReadEncM2(config.address)[1])
	hipAngle = int(rc.ReadEncM1(config.address)[1])
	heelAngle = readPot()
	return kneeAngle, hipAngle, heelAngle

# IN PROGRESS
def readCurrents():
#	kneeCurrent, hipCurrent = [0.01]*2
#	return np.array([[kneeCurrent], [hipCurrent]])
	currents = rc.ReadCurrents(config.address)
	if currents[0]:
		kneeCurrent, hipCurrent = currents[1:] #make sure order is correct
		return np.array([kneeCurrent, hipCurrent]).reshape(2,1)
	else:
		return -10*np.ones((1,2))



# COMPLETE
def calibrate():
	config.calibratedValues = readAngles()
	config.calibrated = True
	print('\tReference Positions: {}\n'.format(config.calibratedValues))
	return


# COMPLETE
def setMotors(pwm_Knee, pwm_Hip):
	rc.ForwardM2(config.address, pwm_Knee) if pwm_Knee >= 0 else rc.BackwardM2(config.address, -pwm_Knee)
	rc.ForwardM1(config.address, pwm_Hip) if pwm_Hip >= 0 else rc.BackwardM1(config.address, -pwm_Hip)
	return

# COMPLETE
def killMotors():
	setMotors(0, 0)
	return




######################### Threading Classes #########################

# COMPLETE
class fallConditionCheck (threading.Thread):
	def __init__(self, killEvent, successEvent):
		threading.Thread.__init__(self)
		self.killEvent = killEvent
		self.successEvent = successEvent
		self.angDiff_thresh = 3
		self.timeInterval = 0.05

	# NOT FINAL CODE; only used as test
#	def run(self):
#		w = 0 # read angle 1
#		x = 0 # read angle 2
#		y = 0 # read angle 3
#		while not self.killEvent.is_set():
#			w += 1 # read angle 1
#			x += 1 # read angle 2
#			y += 1 # read angle 3
#			print(w,x,y)
#			time.sleep(0.2)
#			if y==x==w==2:
#				self.successEvent.set()
#				return

# TODO: modify run() to determine fall condition
# Fall condition: read potentiometer, check if angular velocity above threshold, then run
	def run(self):
		while not self.killEvent.is_set():
			angle1 = readPot() # read potentiometer
			time.sleep(self.timeInterval)
			angle2 = readPot() # read potentiometer
			angDiff = (angle2-angle1)
			#print(angDiff)
			if angDiff > self.angDiff_thresh:
				self.successEvent.set()
				return





######################### Purely Software Functions #########################

# COMPLETE
def genTorqueList():
	config.torqueManager = torqueList.torqueListManager(config.torqueListPath)
	config.torqueListGenerated = True
	return


# COMPLETE
def menuAndCalling(menuOptions):

	numOptions = len(menuOptions)

	# Print option menu
	print('\nOptions:')
	for i in range(numOptions):
	    print('{}. {}'.format(i+1, menuOptions[i+1][0]))
	choice = raw_input('Choice: ')
	print('')

	try:
		choice = int(choice)
		assert choice in range(1,numOptions+1)
	except:
		print('Invalid choice. Choose again.')
		return

	menuOptions[choice][1]()

	rows, columns = os.popen('stty size', 'r').read().split()
	print('*'*int(columns))

	return

# NEEDS WORK; non-bijective system makes this trickier
def getPulseFromAngle(angleKnee, angleHip):
    position_Knee = angleKnee * config.pulsePerRotation/360.0 + config.calibratedValues[0]# + config.pulsePerRotation/4.0
    position_Hip  = angleHip  * config.pulsePerRotation/360.0 + config.calibratedValues[1]# + config.pulsePerRotation/4.0
    return position_Knee, position_Hip


def set_motors():
    # implement way to get feedback on position for this
    # write ascii animation to help move joints into position

    accel = 12000
    speed = 12000
    decel = 12000

    position_Knee, position_Hip = getPulseFromAngle(config.initialAngle_Knee, config.initialAngle_Hip)
    time.sleep(1)
    rc.SpeedAccelDeccelPositionM2(config.address,int(accel),int(speed), int(decel), int(position_Knee), 0)
    rc.SpeedAccelDeccelPositionM1(config.address,int(accel), int(speed), int(decel), int(position_Hip), 0)
    time.sleep(1.5*2)
    print('Knee Angle set to {}'.format(config.initialAngle_Knee))
    print('Hip Angle set to {}'.format(config.initialAngle_Hip))


# COMPLETE
class positionControl (threading.Thread):
    def __init__(self, killEvent):
        threading.Thread.__init__(self)
        self.killEvent = killEvent

    def run(self):
        target_KNEE, target_HIP = getPulseFromAngle(config.initialAngle_Knee, config.initialAngle_Hip)
        dt = 0.02

	print ("Target Knee {}".format(target_KNEE))
	print ("Target Hip {}".format(target_HIP))

        diff_KNEE, diff_HIP = 1e-9, 1e-9
        intError_KNEE, intError_HIP = 0, 0

        kP = 0.8
        kD = 0.1
        kI = 0

        while not self.killEvent.is_set():
        	currentEncoder_KNEE = rc.ReadEncM2(config.address)[1]
        	diff_KNEE, oldDiff_KNEE = (currentEncoder_KNEE - target_KNEE), diff_KNEE
        	propError_KNEE, dervError_KNEE, intError_KNEE, = kP*diff_KNEE, (diff_KNEE - oldDiff_KNEE)/dt, intError_KNEE + diff_KNEE*dt
        	speed_KNEE = int(round(max(min(kP*propError_KNEE + kI*dervError_KNEE + kD*intError_KNEE, 0xFF), -255)))
        	rc.ForwardM2(config.address, abs(speed_KNEE)) if speed_KNEE > 0 else rc.BackwardM2(config.address, abs(speed_KNEE))

        	currentEncoder_HIP = rc.ReadEncM1(config.address)[1]
        	diff_HIP, oldDiff_HIP = (currentEncoder_HIP - target_HIP), diff_HIP
        	propError_HIP, dervError_HIP, intError_HIP, = kP*diff_HIP, (diff_HIP - oldDiff_HIP)/dt, intError_HIP + diff_HIP*dt
        	speed_HIP = int(round(max(min(kP*propError_HIP + kI*dervError_HIP + kD*intError_HIP, 0xFF), -255)))
        	rc.ForwardM1(config.address, abs(speed_HIP)) if speed_HIP > 0 else rc.BackwardM1(config.address, abs(speed_HIP))
		
		print("Encoder Knee {}".format(currentEncoder_KNEE))
                print("Encoder Hip {}".format(currentEncoder_HIP))
	
	killMotors()
				
if __name__ == "__main__":
	while True:
		print readAngles()
		time.sleep(0.2)
