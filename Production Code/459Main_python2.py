
# LOCAL LIBRARIES
import config
import operationFuncs
import fallingStates
import torqueList


if __name__ == "__main__":

	# MENU 1
	menuOptions = { 
		1:('Calibrate', operationFuncs.calibrate),
		2:('Generate Torque List', operationFuncs.genTorqueList),
		3:('Exit', exit)
		}

	while not (config.calibrated and config.torqueListGenerated):
		operationFuncs.menuAndCalling(menuOptions)


	# MENU 2
	menuOptions = { 
		1:('Recalibrate', operationFuncs.calibrate),
		2:('Generate New Torque List', operationFuncs.genTorqueList),
		3:('Initiate Fall Procedure', fallingStates.fallingSM),
		4:('Exit', exit)
		}

	while True:
		operationFuncs.menuAndCalling(menuOptions)