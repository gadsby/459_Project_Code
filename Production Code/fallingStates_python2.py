# TODO:
# 1) Fill in functions with actual control and data collection --> call operationFuncs, uncomment stuff
# 2) Update documentation


import threading
import operationFuncs


# COMPLETE
def push_into_position_func():

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
	return

# COMPLETE
def neutral_state():

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
	return

# COMPLETE
def primed_state():

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



# INCOMPLETE
def falling():

	"""
	Implements control scheme.

		Arguments:
	    	(None)

	    Returns:
	    	Data -- Data stuff

	"""

	print('\nFALLING: Here I go falling!')
	return [0]*5

# INCOMPLETE
def save_data(data):

	"""
	Description.

		Arguments:
	    	Data -- Data stuff

	    Returns:
	    	(None)

	"""

	# Update using old data IO files and functions
	print('\nSAVING: And here I go saving some data (not actually saving data).')
	print('Fake Data: {}'.format(data))



# COMPLETE
def initiateFallMode():

	"""
	Defines and implements falling state machine and controls program flow.

		Arguments:
	    	(None)

	    Returns:
	    	(None)

	"""

	while True:
		# give option to go to neutral, primed, or quit
		nextStep = push_into_position_func()
		if nextStep == 'N': # stay in neutral state
			varNeutral = neutral_state()
			if varNeutral == 'R':
				continue
			elif varNeutral == 'M':
				return
		elif nextStep == 'M': # quit back to Main Menu
			return

		primed_state()
		data = falling()
		save_data(data)
		return


