# State Machine: Preparing to fall
	# Very raw, will not compile, 


import roboclaw as rc

#rc.Open("/dev/cu.usbmodem1411",115200) # LEFT USB
rc.Open("/dev/cu.usbmodem1421",115200) # RIGHT USB

address = 0x80


# start setup

# user input --> zero positions of limbs


def zero_func():

	"""
	Finds values for each encoder to be used as position reference.

		Arguments:
	    	(None)

	    Returns:
	    	ref -- list of reference encoder values

	"""

	ref = [0]*3
    ref[0] = rc.ReadEncM1(address)[1]
    ref[1] = rc.ReadEncM2(address)[1]
    ref[2] = 0 # read Pot Value
    return ref # make this a global? Need to deal with


# user input --> then start trying to reach defined positions
	# while running, return angle values with feedback, tighten string and get setup finalized
	# when ready, return message that everything is good
	# options: go to neutral state, or directly into primed state


def push_into_position_func():

	"""
	Applies constant torques to push apparatus into a specified position.
	Reads config file to get target positions.

		Arguments:
	    	(None)

	    Returns:
	    	nextState -- Desired next state based on user input; 0 for neutral state, 1 for primed state.

	"""


	targets = [0,0] # get from config
	while True:
		# thread 1: position control
			# position control to get to targets from ref, make a separate function?
			# print current positions, with abstracted OKAY range (delete lines and overwrite, keep last 5)
				# if all 3 positions are met, give additional message
		# thread 2: user input
			# get user input, break if condition met
				# choose to go into neutral state, or right into next step

# neutral state
	# idle

def neutral_state():

	"""
	Turns off motors and waits for user input to continue.

		Arguments:
	    	(None)

	    Returns:
	    	(None)

	"""

	# kill motors
	input('Ready to fall?: ')




# user input --> move into primed state
	# check falling conditions continuously
	# if met, initiate falling

def primed_state():

	"""
	Turns off motors and waits for user input to continue.

		Arguments:
	    	(None)

	    Returns:
	    	(None)

	"""


	# define falling conditions
	# loop over falling conditions
		# if falling conditions met, return and pass into falling algorithm


def falling():
	# lots of complicated stuff and controls









# user input --> move into primed state
	# check falling conditions continuously
	# if met, initiate falling

# falling --> control on torques, update torques, return position data

# data save --> save data to properly labelled csv file












