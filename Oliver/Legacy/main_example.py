# this is to be used as a rough cut of what the program main will do

# PYTHON LIBRARIES
import os
import numpy as np

# PROJECT LIBRARIES
import IO_Helpers_459


sourcePath = '/Users/olivergadsby/Desktop/ENPH 459/Results'
sessionDir = IO_Helpers_459.getSessionDir(sourcePath)

while True:
	userInput = input('Press enter to collect data, type \'q\' to quit...\n')
	if userInput == 'q':
		break

	saveName = IO_Helpers_459.getSaveName(sessionDir)

	# do stuff
	print('Doing stuff...')

	#preppingForFall()
	#data = fallingControl()
	#plotTorqueProfile()

	print('Saving to {}'.format(saveName))
 	#IO_Helpers_459.saveData(data, saveName)



	print('\n'*3+'='*75)




exit()
