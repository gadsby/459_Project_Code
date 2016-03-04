# TODO:
# 1) Fill in functions with attempt to minimize # lines in this file
# 2) Deal with passing ref values
# 3) Require calibration to be done before fall


import fallingStates



# Sub-programs to be called in menu

def calibrate_func():
    global ref
    ref = [0]*3 # actually call ref function when doing this
    print('Reference Positions: {}'.format(ref))

def instruct_func():
	print('Instructions')
	# cubic spline interpolation stuff

def readyForFall():
	fallingStates.initiateFallMode()



# Program Main

if __name__ == "__main__":

	print('Welcome!')

	while True:

		# Define available options and functions; tuple in form of ('name', function)
		menuOptions = { 
			1:('Calibrate', calibrate_func),
			2:('Instructions', instruct_func),
			3:('Initiate Fall Procedure', readyForFall),
			4:('Exit', exit)
			}
		numOptions = len(menuOptions)


		# Print option menu
		print('\nOptions:')
		for i in range(numOptions):
		    print('{}. {}'.format(i+1, menuOptions[i+1][0]))
		choice = input('Choice: ')
		print('')


		# Process input and call proper function
		if choice.isnumeric() and int(choice) in range(1,numOptions+1):
			menuOptions[int(choice)][1]()
		else:
			print('Invalid choice. Choose again.')

		print('*'*100)
