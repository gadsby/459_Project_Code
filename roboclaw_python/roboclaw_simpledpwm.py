import time
import roboclaw

#Windows comport name
roboclaw.Open("/dev/cu.usbmodem1411",115200)
#Linux comport name
#roboclaw.Open("/dev/ttyACM0",115200)

address = 0x82

while(1):
	print('Cycle')
	roboclaw.BackwardM1(address,0)
	#roboclaw.BackwardM2(address,255)
	time.sleep(2)
	
	roboclaw.ForwardM1(address,0)
	#roboclaw.BackwardM2(address,255)
	time.sleep(5)

	roboclaw.BackwardM1(address,50)
	#roboclaw.ForwardM2(address,255)
	time.sleep(2)

	#roboclaw.ForwardBackwardM1(address,96)
	#roboclaw.ForwardBackwardM2(address,32)
	#time.sleep(2)
	
	#roboclaw.ForwardBackwardM1(address,32)
	#roboclaw.ForwardBackwardM2(address,96)
	#time.sleep(2)
