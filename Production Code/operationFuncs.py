import threading
import time

import readline,thread
import sys,struct,fcntl,termios



class fallConditionCheck (threading.Thread):
	def __init__(self, killEvent, successEvent):
		threading.Thread.__init__(self)
		self.killEvent = killEvent
		self.successEvent = successEvent

	# NOT FINAL CODE; only used as test
	def run(self):
		w = 0 # read angle 1
		x = 0 # read angle 2
		y = 0 # read angle 3
		while not self.killEvent.is_set():
			w += 1 # read angle 1
			x += 1 # read angle 2
			y += 1 # read angle 3
			print(w,x,y)
			time.sleep(0.5)
			if y==x==w==5:
				self.successEvent.set()
				return


# TODO: modify run() to determine fall condition
#	def run(self):
#		while not self.killEvent.is_set():
#			w = 0 # read angle 1
#			x = 0 # read angle 2
#			y = 0 # read angle 3
#			concurrent_print(w,x,y)
#			time.sleep(0.01)
#			if y > x > w:
#				self.successEvent.set()
#				return





def blank_current_readline():
	# Next line said to be reasonably portable for various Unixes
	(rows,cols) = struct.unpack('hh', fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ,'1234'))
	text_len = len(readline.get_line_buffer())+2

	# ANSI escape sequences (All VT100 except ESC[0G)
	sys.stdout.write('\x1b[2K')                         # Clear current line
	sys.stdout.write('\x1b[1A\x1b[2K'*(text_len/cols))  # Move cursor up and clear line
	sys.stdout.write('\x1b[0G')                         # Move to start of line


def concurrent_print(text, prompt):
	blank_current_readline()
	print(text)
	sys.stdout.write(prompt + readline.get_line_buffer())
	sys.stdout.flush()          # Needed or text doesn't show until a key is pressed