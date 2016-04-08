
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
        motorDetected = rc.Open(port, config.baudRate)
    except:
        continue
if(not motorDetected):
    print('Motor port could not be opened.')
    print('Ports checked:')
    for i in config.comPorts:
    	print('\t'+i)
 	 print('Exiting...')
    exit()


# INITIALIZE GPIO PORTS
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

# IN PROGRESS; ALMOST COMPLETE
def readAngles():
	kneeAngle = rc.ReadEncM1()
	hipAngle = rc.ReadEncM2()
	heelAngle = readPot()
	return kneeAngle, hipAngle, heelAngle

# IN PROGRESS
def readCurrents():
#	kneeCurrent, hipCurrent = [0.01]*2
#	return np.array([[kneeCurrent], [hipCurrent]])
	currents = rc.ReadCurrents()
	if currents[0]:
		kneeCurrent, hipCurrent = currents[1:] #make sure order is correct
		return np.array([kneeCurrent, hipCurrent])
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
	rc.ForwardM1(config.address, pwm_Knee) if pwm_Knee >= 0 else rc.BackwardM1(config.address, -pwm_Knee)
	rc.ForwardM2(config.address, pwm_Hip) if pwm_Hip >= 0 else rc.BackwardM2(config.address, -pwm_Hip)
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
		self.angVel_thresh = 0
		self.timeInterval = 0.01

	# NOT FINAL CODE; only used as test
	def run(self):
		w = 0 # read angle 1
		x = 0 # read angle 2
		y = 0 # read angle 3
		while not self.killEvent.is_set():
			w += 1 # read angle 1
			x += 1 # read angle 2
			y += 1 # read angle 3
			print(w,x,y)
			time.sleep(0.2)
			if y==x==w==2:
				self.successEvent.set()
				return

# TODO: modify run() to determine fall condition
# Fall condition: read potentiometer, check if angular velocity above threshold, then run
#	def run(self):
#		while not self.killEvent.is_set():
#			angle1 = readPot() # read potentiometer
#			time.sleep(self.timeInterval)
#			angle2 = readPot() # read potentiometer
#			angVel = (angle2-angle1)/self.timeInterval
#			print(angVel)
#			if angVel > self.angVel_thresh:
#				self.successEvent.set()
#				return





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






