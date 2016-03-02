import os
import time
import datetime
import csv

dir_path = 'C:/TestFolder'

def gen_time_stamp():
	"""
	Generate current date_stamp
	"""
	time_stamp = time.time()
	date_stamp = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H-%M-%S')
	return date_stamp

def gen_directory(dir_path):
	"""
	@param	string	dir_path	directory path
	"""
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

def write_to_csv(path, filename, data):
	"""
	@param string 	path 		path of the file
	@param string	filename	name of the file
	@param list 	data 		data being written to the file as an array
	@return			void
	"""
	#Generate full file path
	file_path = path + "/" + filename + ".csv"
	
	#Open a file with the passed filename
	file = open(file_path, 'a')

	#Write Data to File
	wr = csv.writer(file, quoting=csv.QUOTE_NONE, lineterminator='\n')
	wr.writerow(data)

	#Close the File Name
	file.close()

#Generate CSV
filename = "test_file"

gen_directory(dir_path)
write_to_csv(dir_path, filename, [1,2,3])