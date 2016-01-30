import roboclaw

#Windows comport name
roboclaw.Open("/dev/cu.usbmodem1411",115200)
#Linux comport name
#roboclaw.Open("/dev/ttyACM0",115200)

address = 0x80

print roboclaw.ReadM1PositionPID(address)