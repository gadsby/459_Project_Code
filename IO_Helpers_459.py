# DATA SAVING LIBRARY


def getSessionDir():

	"""getSessionDir: Returns the directory for a given session to be used for saving new files. Previous session IDs are checked and a unique ID is created.

	Arguments:
	(none)
	"""

	import datetime
	import os

	#TODO: will be set by file structure, maybe use proper config? put in main?
	sourcePath = '/Users/olivergadsby/Desktop/Example'

	#TODO: set as constant; 1 for Jan3-Jan9 start, maybe use proper config?
	projectWeekStart = 1

	today = datetime.date.today()

	weekNum = today.isocalendar()[1]
	projectWeek = weekNum - projectWeekStart

	modWeekDay = (today.weekday() + 1) % 7
	weekStart = (today - datetime.timedelta(modWeekDay)).strftime("%b%d")
	weekEnd = (today + datetime.timedelta(6-modWeekDay)).strftime("%b%d")

	weekDir = 'week{0:02d}_{1:s}-{2:s}'.format(projectWeek, weekStart, weekEnd)
	weekDir = '{}/{}'.format(sourcePath, weekDir)

	if not os.path.isdir( weekDir ):
		os.mkdir( weekDir )

	dirNums = [int(f.split('session_')[1]) for f in os.listdir(weekDir) if f.startswith('session_')]
	if len(dirNums) == 0:
		sessionNum = 1	
		sessionDir = '{0:s}/session_{1:02d}'.format(weekDir, sessionNum)	
	else:
		sessionNum = max(dirNums)
		sessionDir = '{0:s}/session_{1:02d}'.format(weekDir, sessionNum)
		if len(os.listdir(sessionDir)) != 0:
			sessionNum += 1
			sessionDir = '{0:s}/session_{1:02d}'.format(weekDir, sessionNum)

	if not os.path.isdir( sessionDir ):
		os.mkdir( sessionDir )

	return sessionDir



def getSaveName(path):

	"""Returns the name of the next valid file. Previous files are checked and a unique ID is created.

	Arguments:
	path -- directory for the current session, found from getSessionDir()
	"""

	import datetime
	import os

	fileNums = [int(f.split('_')[0]) for f in os.listdir(path) if f.endswith('.csv')]

	if len(fileNums) == 0:
		fileNum = 1		
	else:
		fileNum = max(fileNums) + 1	

	timestamp = datetime.datetime.now().strftime("%a_%H_%M_%S")
	saveName = '{0:s}/{1:02d}_{2:s}.csv'.format(path, fileNum, timestamp)

	return saveName


#TODO: complete this
# pass data to be saved and then save to a properly named CSV with the full filename path on the first line
def saveData(data, filename):
	"""DOCSTRING PLACEHOLDER"""
	pass



if __name__ == "__main__":
	print( getSessionDir.__doc__ )
	print( getSaveName.__doc__ )
	print( saveData.__doc__ )



# file structure:
#
# sourceDir/						# defined from beginning, hardcoded
#	week01_MonDD-MonDD/				# made each week
#		session_01/					# made each session
#			01_Day_HH_MM_SS.csv 	# made for each save call, timestamp ex. Mon_23_59_59
#			02_Day_HH_MM_SS.csv
#			03_Day_HH_MM_SS.csv
#			04_Day_HH_MM_SS.csv


