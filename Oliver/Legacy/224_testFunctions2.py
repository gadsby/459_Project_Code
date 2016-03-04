

# Sub-programs to be called in menu

def zero_func():
    print('Zero')

def instruct_func():
	print('Instructions')
	torqueList = read_torque_CSV(fileAddress)

def primeForFall_func():
	print('Prime for Falling')

	while not fallInitiated():
		continue

	data = falling_func()
	save_data(data)

def falling_func():

	falling = True

	while falling:
		torqueVals = getTorqueTarget()
		controlMotors(torqueVals)
		tempData = readSensors()
		data = appendData(data, tempData)

		if condition:
			falling = False
			return data