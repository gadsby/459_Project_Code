# needs improvement to structure, consistency, and documentation, but state transitions work

# TODO:
# 1) Fill in functions with actual control and data collection
# 2) Add documentation
# 3) Clean up style
# 4) Convert to Python 2



# TODO: put back to Main Menu option (DONE)
# TODO: improve Main Menu option
def push_into_position_func():
	print('')
	while True:
		var = input('Options: N (Neutral) / P (Primed) / M (Main Menu)\n')
		if var in ['N', 'P', 'M']:
			return var
		else:
			print('Invalid. Choose \'N\', \'P\', or \'M\'.\n')

# TODO: put switch to neutral option (DONE)
def primed_state():
	print('\nPRIMED: Apparatus is primed and awaiting fall conditions to be met.\n\
		Press \'N\' to go to neutral state.')
	var = input('Press any other key and <ENTER> to simulate start of fall.\n')
	if var == 'N':
		return var
	return 0

# TODO: put switch options for main menu and push_into_position_func (DONE)
def neutral_state():
	print('\nNEUTRAL: Apparatus is set to neutral and awaiting feedback to transition to primed state.\n\
		Press \'M\' to go to the main menu, or \'R\' to restart falling scheme.')
	var = input('Press any other key and <ENTER> to move into primed state.\n')
	if var in ['M', 'R']:
		return var
	else:
		return 0

def falling():
	print('\nFALLING: Here I go falling!')
	return [0]*5

def save_data(data):
	print('\nSAVING: And here I go saving some data (not actually saving data).')
	print('Fake Data: {}'.format(data))
	return






def initiateFallMode():
	while True:
		nextStep = push_into_position_func()

		back2Start = False

		# give option to go to neutral, primed, or quit
		if nextStep == 'N': # stay in neutral state
			varNeutral = neutral_state()
			if varNeutral == 'R':
				continue
			elif varNeutral == 'M':
				return

		elif nextStep == 'M': # quit back to Main Menu
			return

		while True:
			if primed_state() == 'N':
				varNeutral = neutral_state()
				if varNeutral == 'R':
					back2Start = True
					break
				elif varNeutral == 'M':
					return
			else:
				break

		if back2Start:
			continue

		data = falling()
		save_data(data)
		return


