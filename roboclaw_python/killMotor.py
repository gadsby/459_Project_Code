import roboclaw

roboclaw.Open("/dev/cu.usbmodem1411",115200)
address = 0x82

print('Stopping...')
roboclaw.ForwardM1(address,0)
roboclaw.ForwardM2(address,0)