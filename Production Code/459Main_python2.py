# TODO:
# 1) Fill in functions with attempt to minimize # lines in this file
# 2) Deal with passing ref values
# 3) Require calibration to be done before fall


import fallingStates_python2



# Sub-programs to be called in menu

def calibrate_func():
    global ref
    ref = [0]*3 # actually call ref function when doing this
    print('Reference Positions: {}'.format(ref))

def instruct_func():
	print('Instructions')
	# cubic spline interpolation stuff

def readyForFall():
	fallingStates_python2.initiateFallMode()




def menuAndCalling():
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

	print('*'*100)



# Program Main

if __name__ == "__main__":

	print('\nENPH 459: Group 1617')

	# MENU 1
	# Define available options and functions; tuple in form of ('name', function)
	menuOptions = { 
		1:('Calibrate', calibrate_func),
		2:('Exit', exit)
		}
	numOptions = len(menuOptions)

	while True:
		menuAndCalling()
		if 'ref' in globals():
			break


	# MENU 2
	# Define available options and functions; tuple in form of ('name', function)
	menuOptions = { 
		1:('Calibrate', calibrate_func),
		2:('Instructions', instruct_func),
		3:('Initiate Fall Procedure', readyForFall),
		4:('Exit', exit)
		}
	numOptions = len(menuOptions)

	while True:
		menuAndCalling()


