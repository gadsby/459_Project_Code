# TODO:
# 1) Fill in functions with actual control and data collection --> uncomment stuff
# 2) Update documentation


import operationFuncs
import dataSaving
import config

#import roboclaw as rc

import time
import threading
import numpy as np



class fallingSM:

	dataSizeTuple = (250000, 6)
	metadataNames = ['torqueListPath', 'kp', 'kd', 'ki', 'shankLength', 'thighLength',
	 'trunkLength', 'shankMass', 'thighMass', 'trunkMass', 'initialAngle_Knee',
	  'initialAngle_Hip', 'calibratedValues']	

	def __init__(self):

		self.fallingData = np.zeros(fallingSM.dataSizeTuple)
		self.initiateFallMode()


	# STATE MACHINE IMPLEMENTATION
	def initiateFallMode(self):

		"""
		Defines and implements falling state machine and controls program flow.

			Arguments:
				(None)

			Returns:
				(None)

		"""

		while True:
			# give option to go to neutral, primed, or quit
			nextStep = self.push_into_position_func()
			if nextStep == 'N': # stay in neutral state
				varNeutral = self.neutral_state()
				if varNeutral == 'R':
					continue
				elif varNeutral == 'M':
					return
			elif nextStep == 'M': # quit back to Main Menu
				return

			self.primed_state()
			self.falling()
			self.save_data()
			return


	# STATE 1
	def push_into_position_func(self):

		"""
		Applies constant torques to push apparatus into a specified position.
		Reads config file to get target positions relative to calibrated values.

			Arguments:
				(None)

			Returns:
				nextState -- Desired next state based on user input; 'N' for Neutral, 'P' for Primed, 'M' for Main Menu.

		"""


		#operationFuncs.set_motors()
		print('\nSTARTING: Apparatus is powered and being pushed into position for fall.')
		while True:
			var = raw_input('Options: N (Neutral) / P (Primed) / M (Main Menu)\n')
			if var in ['N', 'P', 'M']:
				return var
			else:
				print('Invalid. Choose \'N\', \'P\', or \'M\'.\n')


	# WAIT STATE
	def neutral_state(self):

		"""
		Turns off motors and waits for user input to continue.

			Arguments:
				(None)

			Returns:
				nextState -- Desired next state based on user input; 'M' for Main Menu, 'R' to Restart control loop.

		"""

		#operationFuncs.killMotors()
		print('\nNEUTRAL: Apparatus is set to neutral and awaiting feedback to restart.')
		while True:
			var = raw_input('Options: M (Main Menu) / R (Restart Falling)\n')
			if var in ['M', 'R']:
				return var
			else:
				print('Invalid. Choose \'M\', or \'R\'.\n')


	# STATE 2
	def primed_state(self):

		"""
		Checks to see if falling condition is met, then transitions to falling.

			Arguments:
				(None)

			Returns:
				(None)

		"""

		print('\nPRIMED: Apparatus is primed and awaiting fall conditions to be met.')

		killCondition = threading.Event()
		successCondition = threading.Event()

		fallChecker = operationFuncs.fallConditionCheck(killCondition, successCondition)
		fallChecker.start()

		while not successCondition.is_set():
			continue

		killCondition.set()

		return


	# STATE 3 (IN PROGRESS)
	def falling(self):

		"""
		Implements control scheme.

			Arguments:
				(None)

			Returns:
				Data -- Data structure to be saved

		"""

		print('\nFALLING: Here I go falling!')

		lastError_Knee, lastError_Hip, pwm_Knee, pwm_Hip, dataIndex = [0]*5

		timeStart = time.clock()
		timeNow = 0

		while True:
			
			kneeTorqueGoal, hipTorqueGoal = config.torqueManager.torqueGoals(timeNow)

			# READ DATA FROM SENSORS (IN PROGRESS)
			kneeAngle, hipAngle, heelAngle = operationFuncs.readAngles()
			hipTorque = 0 # ?
			kneeTorque = 0 # ?


			# ASSIGN DATA TO DATA ARRAY
			self.fallingData[dataIndex, :] = [timeNow, heelAngle, kneeAngle, hipAngle, hipTorque, kneeTorque]
			dataIndex += 1

			# CONTROL PORTION (IN PROGRESS)






			# DEFINE PWM OUTPUT (IN PROGRESS)
			pwm_Knee = 0 # some function of control variables
			pwm_Hip = 0 # some function of control variables

			# CONTROL JOINTS
			#rc.ForwardM1(config.address, pwm_Knee) if pwm_Knee >= 0 else rc.BackwardM1(config.address, -pwm_Knee)
			#rc.ForwardM2(config.address, pwm_Hip) if pwm_Hip >= 0 else rc.BackwardM2(config.address, -pwm_Hip)

			timeNow = time.clock() - timeStart

			if timeNow > config.torqueManager.timeLimit:
				break

		#operationFuncs.killMotors()
		self.fallingData = self.fallingData[:dataIndex]

		return



	# STATE 4
	def save_data(self):

		"""
		Takes data and saves in format specified by dataSaving module.

			Arguments:
				Data -- Data to be saved
				Directory -- Base directory to be used for saving (defined by settings, date)

			Returns:
				(None)

		"""

		ioStructure = dataSaving.ioOperations(config.dataFolder)
		sessionDirectory = ioStructure.getSaveName()

		fileName, fullPath = ioStructure.getSaveName()

		metadata = '\n'.join(['{}\t{}'.format(name, eval('config.'+name)) for name in fallingSM.metadataNames])

		np.savetxt(fullPath, self.fallingData, delimiter=',', header=metadata, comments='')

		print('\nSAVING: And here I go saving some data (not actually saving real data).')
		print('Data Saved!\n')
		print('\tSize {}'.format(self.fallingData.shape))
		print('\t{} lines of metadata'.format(len(metadataNames)))
		print('\tPath name: {}\n'.format(fileName))

		return



