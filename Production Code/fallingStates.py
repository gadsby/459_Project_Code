# TODO:
# 1) Fill in functions with actual control and data collection --> uncomment stuff, add control loop
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
		print('\nSTARTING!')
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

		print('\nPRIMED!')

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
		angVel_knee, angVel_hip, angVel_heel = operationFuncs.readAngles() # that's not right
		angAcc_knee, angAcc_hip, angAcc_heel = [0]*3

		L = 1.60  # Total height of the human subject
		M = 53.7  # Total mass of the human subject
		L0 = 0.039*L # foot height
		L1 = (0.285-0.039)*L # Shank length
		L2 = (0.53-0.285)*L # Thigh length
		L3 = (0.818-0.53)*L # Trunk length
		L4 = (1-0.818)*L # Head and neck length
		rCOM_1 = 0.394 # Distal distance of center of mass of the foot and shank segment given as a percent of shank length
		rCOM_2 = 0.567 # Distal distance of center of mass of the thigh segment given as a percent of thigh length
		rCOM_3 = 0.626 # Proximal distance of center of mass of the HAT (Head, Arms, Trunk) segment given as a percent of trunk length
		rG_1 = 0.572 # Distal radius of gyration of the foot and shank segment given as a percent of shank length
		rG_2 = 0.653 # Distal radius of gyration of the thigh segment given as a percent of thigh length
		rG_3 = 0.798 # Proximal radius of gyration of HAT segment given as percent of trunk length
		M1 = 0.061*M # Foot and shank mass
		M2 = 0.1*M # Thigh mass
		M3 = 0.5*(0.678*M) # Half the mass of the HAT segment
		g = 9.8 # gravitational acceleration

		timeStart = time.clock()
		timeNow = 0

		while True:
			
			kneeTorqueGoal, hipTorqueGoal = config.torqueManager.torqueGoals(timeNow)

			# READ DATA FROM SENSORS AND CALCULATE DERIVED DATA (IN PROGRESS)
			last_kneeAngle, last_hipAngle, last_heelAngle = kneeAngle, hipAngle, heelAngle
			kneeAngle, hipAngle, heelAngle = operationFuncs.readAngles()

			last_angVel_knee, last_angVel_hip, last_angVel_heel = angVel_knee, angVel_hip, angVel_heel
			angVel_knee, angVel_hip, angVel_heel = np.array([kneeAngle-last_kneeAngle,
				hipAngle-last_hipAngle, heelAngle-last_heelAngle]) / 1.0 #timeStepSize, time since last fall

			last_angAcc_knee, last_angAcc_hip, last_angAcc_heel = angAcc_knee, angAcc_hip, angAcc_heel
			angAcc_knee, angAcc_hip, angAcc_heel = np.array([angVel_knee-last_angVel_knee, 
				angVel_hip-last_angVel_hip, angVel_heel-last_angVel_heel]) / 1.0 #timeStepSize




			a11 = M1 * rG_1**2 * L1**2 + M2 * (rG_2**2 * L2**2 + (L0+L1)**2 + 2 * rCOM_2 * (L0 + L1) * L2 * np.cos(kneeAngle))\
			    + M3 * (rG_3**2 * L3**2 + L2**2 + (L0 + L1)**2 + 2 * rCOM_3 * L3 * L2 * np.cos(hipAngle) + 2 * L2 * (L0 + L1) * np.cos(kneeAngle)\
			    + 2 * rCOM_3 * (L0 + L1) * L3 * np.cos(kneeAngle + hipAngle))
			a12 = M2 * (rG_2**2 * L2**2 + rCOM_2 * (L0 + L1) * L2 * np.cos(kneeAngle))\
			    + M3 * (rG_3**2 * L3**2 + L2**2 + 2 * rCOM_3 * L3 * L2 * np.cos(hipAngle) + L2 * (L0 + L1) * np.cos(kneeAngle)\
			    + rCOM_3 * (L0 + L1) * L3 * np.cos(kneeAngle + hipAngle))
			a13 = M3 * (rG_3**2 * L3**2 + rCOM_3 * L3 * L2 * np.cos(hipAngle) + rCOM_3 * (L0 + L1) * L3 * np.cos(kneeAngle + hipAngle));
			a21 = M2 * (rG_2**2 * L2**2 + rCOM_2 * (L0 + L1) * L2 * np.cos(kneeAngle))\
			    + M3 * (rG_3**2 * L3**2 + L2**2 + 2 * rCOM_3 * L2 * L3 * np.cos(hipAngle) + (L0 + L1) * L2 * np.cos(kneeAngle) + rCOM_3 * (L0 + L1) * L3 * np.cos(kneeAngle + hipAngle))
			a22 = rG_2**2 * M2 * L2**2\
			    + M3 * (rG_3**2 * L3**2 + L2**2 + 2 * rCOM_3 * L2 * L3 * np.cos(hipAngle))
			a23 = M3 * (rG_3**2 * L3**2 + rCOM_3 * L2 * L3 * np.cos(hipAngle))
			a31 = M3 * (rG_3**2 * L3**2 + rCOM_3 * L3 * L2 * np.cos(hipAngle) + rCOM_3 * L3 * (L0 + L1) * np.cos(kneeAngle + hipAngle))
			a32 = M3 * (rG_3**2 * L3**2 + rCOM_3 * L3 * L2 * np.cos(hipAngle))
			a33 = M3 * rG_3**2 * L3**2	

			c11 = M3 * (2 * rCOM_3 * L2 * L3 * np.sin(hipAngle) * angVel_hip + 2 * L2 * (L0 + L1) * np.sin(kneeAngle) * angVel_knee
			    + 2 * rCOM_3 * (L0 + L1) * L3 * np.sin(kneeAngle + hipAngle) * (angVel_knee + angVel_hip)) * angVel_heel\
			    + M3 * (2 * rCOM_3 * L2 * L3 * np.sin(hipAngle) * angVel_hip + L2 * (L0 + L1) * np.sin(kneeAngle) * angVel_knee
			    + rCOM_3 * (L0 + L1) * L3 * np.sin(kneeAngle + hipAngle) * (angVel_knee + angVel_hip)) * angVel_knee\
			    + M3 * (rCOM_3 * L2 * L3 * np.sin(hipAngle) * angVel_hip + rCOM_3 * (L0 + L1) * L3 * np.sin(kneeAngle + hipAngle) * (angVel_knee + angVel_hip)) * angVel_hip\
			    + M2 * (2 * rCOM_2 * L2 * (L0 + L1) * np.sin(kneeAngle) * angVel_heel * angVel_knee + rCOM_2 * (L0 + L1) * L2 * np.sin(kneeAngle) * angVel_knee**2)\
			    - rCOM_1 * M1 * L1 * g * np.cos(heelAngle) - (M2 + M3) * (L0 + L1) * g * np.cos(heelAngle) - (rCOM_2 * M2 + M3) * L2 * g * np.cos(heelAngle + kneeAngle)\
			    - rCOM_3 * M3 * g * L3 * np.cos(heelAngle + kneeAngle + hipAngle)
			c21 = M3 * (2 * rCOM_3 * L3 * L2 * np.sin(hipAngle) * angVel_hip + L2 * (L0 + L1) * np.sin(kneeAngle) * angVel_knee\
			    + rCOM_3 * (L0 + L1) * L3 * np.sin(kneeAngle + hipAngle) * (angVel_knee + angVel_hip)) * angVel_heel\
			    + M3 * 2 * rCOM_3 * L3 * L2 * np.sin(hipAngle) * angVel_hip * angVel_knee\
			    + M3 * rCOM_3 * L3 * L2 * np.sin(hipAngle) * angVel_hip * angVel_hip\
			    + M2 * rCOM_2 * L2 * (L0 + L1) * np.sin(kneeAngle) * angVel_heel * angVel_knee\
			    - M3 * (((L0 + L1) * L2 * np.sin(kneeAngle) + rCOM_3 * L0 + L1) * L3 * np.sin(kneeAngle + hipAngle)) * (angVel_knee + angVel_heel)\
			    + (rCOM_3 * L3 * (L0 + L1) * np.sin(kneeAngle + hipAngle) * angVel_hip) * angVel_heel\
			    - M2 * rCOM_2 * L2 * (L0 + L1) * np.sin(kneeAngle) * angVel_heel * (angVel_heel + angVel_knee)\
			    - (rCOM_2 * M2 + M3) * L2 * g * np.cos(heelAngle + kneeAngle) - (rCOM_3 * M3) * L3 * g * np.cos(heelAngle + kneeAngle + hipAngle)
			c31 = M3 * (rCOM_3 * L3 * L2 * np.sin(hipAngle) * angVel_hip + rCOM_3 * L3 * (L0 + L1) * np.sin(kneeAngle + hipAngle) * (angVel_knee + angVel_hip)) * angVel_heel\
			    + M3 * (rCOM_3 * L3 * L2 * np.sin(hipAngle) * angVel_hip) * angVel_knee\
			    - M3 * rCOM_3 * L3 * (angVel_heel + angVel_knee + angVel_hip) * (angVel_heel * (L2 * np.sin(hipAngle) + (L0 + L1) * np.sin(kneeAngle + hipAngle)) + L2 * angVel_knee * np.sin(hipAngle))			

			A = np.matrix([[a11, a12, a13],[a21, a22, a23],[a31, a32, a33]])
			C = np.matrix([[c11], [c21], [c31]])




# characterize frictional torque vs. angVel
# input findings into c21 and c31 --> a*angVel
# find inertia of rotor, combine 2 inertias --> (v1/v2)^2, in frame of output shaft
# inertia of rotor, inertia of mechanical system (aii, only diagonals)

			kneeTorque = 1 # to be updated
			hipTorque = 1 # to be updated


			# ASSIGN DATA TO DATA ARRAY
			self.fallingData[dataIndex, :] = [timeNow, heelAngle, kneeAngle, hipAngle, hipTorque, kneeTorque]
			dataIndex += 1

			# CONTROL PORTION; DEFINE PWM OUTPUT (IN PROGRESS)
			diff_knee = kneeTorque - kneeTorqueGoal
			pwm_Knee = config.kp['knee'] * diff_knee

			diff_hip = hipTorque - hipTorqueGoal
			pwm_Hip = config.kp['hip'] * diff_hip

			# DEFINE CLIPPING
			pwm_Knee = np.sign(pwm_Knee)*255 if abs(pwm_Knee) > 255 else pwm_Knee
			pwm_Hip = np.sign(pwm_Hip)*255 if abs(pwm_Hip) > 255 else pwm_Hip

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

		print('\nSAVING!')

		ioStructure = dataSaving.ioOperations(config.dataFolder)
		sessionDirectory = ioStructure.getSaveName()

		fileName, fullPath = ioStructure.getSaveName()


		metadataList = ['{}\t{}'.format(name, eval('config.'+name)) for name in fallingSM.metadataNames]
		metadataForFile = '\n'.join(metadataList)
		metadataForPrinting = '\t' + '\n\t'.join(metadataList)
		print(metadataForPrinting)

		np.savetxt(fullPath, self.fallingData, delimiter=',', header=metadataForFile, comments='')

		print('\nData Saved!')
		print('\tSize {}'.format(self.fallingData.shape))
		print('\t{} lines of metadata'.format(len(fallingSM.metadataNames)))
		print('\tPath name: {}\n'.format(fileName))

		return



