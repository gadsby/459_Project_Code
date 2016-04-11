
# LOCAL LIBRARIES
import operationFuncs
import dataSaving
import config

# PYTHON LIBRARIES
import time
import threading
import numpy as np



class fallingSM:

	dataSizeTuple = (250000, 6)

	def __init__(self):

		self.fallingData = np.zeros(fallingSM.dataSizeTuple)
		self.initiateFallMode()


	# STATE MACHINE IMPLEMENTATION (COMPLETE)
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


	# STATE 1 (COMPLETE)
	def push_into_position_func(self):

		"""
		Applies constant torques to push apparatus into a specified position.
		Reads config file to get target positions relative to calibrated values.

			Arguments:
				(None)

			Returns:
				nextState -- Desired next state based on user input; 'N' for Neutral, 'P' for Primed, 'M' for Main Menu.

		"""


		operationFuncs.set_motors()
		print('\nSTARTING!')
		while True:
			var = raw_input('Options: N (Neutral) / P (Primed) / M (Main Menu)\n')
			if var in ['N', 'P', 'M']:
				return var
			else:
				print('Invalid. Choose \'N\', \'P\', or \'M\'.\n')


	# WAIT STATE (COMPLETE)
	def neutral_state(self):

		"""
		Turns off motors and waits for user input to continue.

			Arguments:
				(None)

			Returns:
				nextState -- Desired next state based on user input; 'M' for Main Menu, 'R' to Restart control loop.

		"""

		operationFuncs.killMotors()
		print('\nNEUTRAL: Apparatus is set to neutral and awaiting feedback to restart.')
		while True:
			var = raw_input('Options: M (Main Menu) / R (Restart Falling)\n')
			if var in ['M', 'R']:
				return var
			else:
				print('Invalid. Choose \'M\', or \'R\'.\n')


	# STATE 2 (COMPLETE)
	def primed_state(self):

		"""
		Checks to see if falling condition is met, then transitions to falling.

			Arguments:
				(None)

			Returns:
				(None)

		"""

		print('\nPRIMED!')

		# threading isn't really at all important here; should probably change this
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

		print('\nFALLING!\n')

		lastError_Knee, lastError_Hip, pwm_Knee, pwm_Hip, dataIndex = [0]*5

		kneeAngle, hipAngle, heelAngle = config.calibratedValues
		angVel_knee, angVel_hip, angVel_heel = [0]*3
		angAcc_knee, angAcc_hip, angAcc_heel = [0]*3

		intError = np.zeros((2,1))
		intErrorMax = 1000

		timeStart, timeLast = time.time(), 0
		timeNow, timeStep = time.time() - timeStart, 10e-9 # initialize timeStep as small value

		while True:
			
			# READ PRECOMPUTED DATA FROM MEMORY
			desiredTorques, torqueResponses, controlMat = config.torqueManager.torqueGoals(timeNow)

			# READ DATA FROM SENSORS AND CALCULATE DERIVED DATA
			last_kneeAngle, last_hipAngle, last_heelAngle = kneeAngle, hipAngle, heelAngle
			kneeAngle, hipAngle, heelAngle = operationFuncs.readAngles()

			last_angVel_knee, last_angVel_hip, last_angVel_heel = angVel_knee, angVel_hip, angVel_heel
			angVel_knee, angVel_hip, angVel_heel = np.array([kneeAngle-last_kneeAngle,
				hipAngle-last_hipAngle, heelAngle-last_heelAngle]) / timeStep

			last_angAcc_knee, last_angAcc_hip, last_angAcc_heel = angAcc_knee, angAcc_hip, angAcc_heel
			angAcc_knee, angAcc_hip, angAcc_heel = np.array([angVel_knee-last_angVel_knee, 
				angVel_hip-last_angVel_hip, angVel_heel-last_angVel_heel]) / timeStep

			# get lastPwm to give sign of currents

			actualTorques = config.torque_motorConstant * operationFuncs.readCurrents()

			# CONTROL OPERATIONS
			EM_torqueFeedback_adjust = actualTorques - torqueResponses
			EM_torque_adjust = desiredTorques - torqueResponses
			errorNow = EM_torque_adjust - EM_torqueFeedback_adjust

	#		print(actualTorques.shape, actualTorques)
	#		print EM_torqueFeedback_adjust.shape, EM_torqueFeedback_adjust
	#		print torqueResponses.shape, torqueResponses
	#		print EM_torque_adjust.shape, EM_torque_adjust
	#		print desiredTorques.shape, desiredTorques
	#		
	#		print(errorNow.shape, errorNow)
	#		print(intError.shape, intError)
			# INTEGRAL ERROR
			intError += errorNow*timeStep
			#intError = [(i/abs(i)) * intErrorMax for i in intError if abs(i) > intErrorMax]
			outputVoltages = np.dot(controlMat, intError)

			# GET PWM INPUT FROM VOLTAGES
			mapVoltageToByte = lambda x: (int(x) * 255) // 12
			byteClipping = lambda x: int(np.sign(x))*255 if abs(x) > 255 else x
			pwm_Knee, pwm_Hip = map(byteClipping, map(mapVoltageToByte, outputVoltages))

			# CONTROL JOINTS
			operationFuncs.setMotors(pwm_Knee=pwm_Knee, pwm_Hip=pwm_Hip)

			# ASSIGN DATA TO DATA ARRAY
			unpackList = lambda list2Unpack: [list2Unpack[0][0],list2Unpack[1][0]]
			self.fallingData[dataIndex, :] = [timeNow, kneeAngle, hipAngle, heelAngle] + unpackList(actualTorques.tolist())
			dataIndex += 1

			# UPDATE TIME CONDITIONS
			timeLast, timeNow = timeNow, time.time() - timeStart
			timeStep = timeNow - timeLast
			if timeNow > config.torqueManager.timeLimit:
				break

		operationFuncs.killMotors()

		self.fallingData = self.fallingData[:dataIndex]

		return



	# STATE 4 (COMPLETE)
	def save_data(self):

		"""
		Takes data and saves in format specified by dataSaving module.

			Arguments:
				Data -- Data to be saved
				Directory -- Base directory to be used for saving (defined by settings, date)

			Returns:
				(None)

		"""

		print('\nSAVING!')

		ioStructure = dataSaving.ioOperations(config.dataFolder)
		fileName, fullPath = ioStructure.getSaveName()


		metadataList = ['{}\t{}'.format(name, eval('config.'+name)) for name in config.metadataNames]
		metadataForFile = '\n'.join(metadataList)
		metadataForPrinting = '\t' + '\n\t'.join(metadataList)
		print(metadataForPrinting)

		np.savetxt(fullPath, self.fallingData, delimiter=',', header=metadataForFile, comments='')

		print('\nData Saved!')
		print('\tSize {}'.format(self.fallingData.shape))
		print('\t{} lines of metadata'.format(len(config.metadataNames)))
		print('\tPath name: {}\n'.format(fileName))

		return



