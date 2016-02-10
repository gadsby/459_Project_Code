
# Sub-programs to be called in menu

def zero_func():
    print('Zero')

def instruct_func():
	print('Instructions')

def primeForFall_func():
	print('Prime for Falling')



# Program Main

if __name__ == "__main__":

	print('Welcome!')

	while True:

		# Define available options and functions; tuple in form of ('name', function)
		menuOptions = { 
			1:('Zero', zero_func),
			2:('Instructions', instruct_func),
			3:('Prime for Falling', primeForFall_func),
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

