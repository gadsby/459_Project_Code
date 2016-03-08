import config
import torqueList

import roboclaw as rc

import threading
import time
import os



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
#			angle1 = 0 # read potentiometer
#			time.sleep(self.timeInterval)
#			angle2 = 0 # read potentiometer
#			angVel = (angle2-angle1)/self.timeInterval
#			print(angVel)
#			if angVel > self.angVel_thresh:
#				self.successEvent.set()
#				return



# IN PROGRESS
def readAngles():
	kneeAngle = 14 #rc.ReadEncM1()
	hipAngle = 14 #rc.ReadEncM2()
	heelAngle = 14 # read GPIO
	return hipAngle, kneeAngle, heelAngle


# COMPLETE
def calibrate():
	config.calibratedValues = readAngles()
	config.calibrated = True
	print('\tReference Positions: {}\n'.format(config.calibratedValues))
	return

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

#def killMotors():
#    rc.ForwardM1(config.address,0)
#    rc.ForwardM2(config.address,0)
