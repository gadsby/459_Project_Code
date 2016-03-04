#<<<<<<< Updated upstream
import time
import serial
import roboclaw as rc
import RPi.GPIO as GPIO
import numpy as np
import instructions

# Fall button is depressed while holding the top link (place physical button there) and open when released

FALL_BUTTON = 8

# modified PID values

_kp = 1
_kd = 0
_ki = .1
_kw = 1

timing = 10
lastError1 = 0
lastError2 = 0
PWM1 = 0
PWM2 = 0
increment1 = 0
increment2 = 0


GPIO.setup(FALL_BUTTON,GPIO.IN)

rc.Open("COM5",115200)
address = 0x80

# Toggle switch to activate mode where system will attempt fall once fall button is released

while FALL_BUTTON == 0 & toggle == 0:

    beginning = time.clock()
    # to shift targets down initialize count as something else
    count = 0
    index = 0

    # Beginning of fall to end of fall all within 1 second, else cut motors
    while time.clock-beginning < 1:

        targets = instructions.targets(index)
        SeekNext(targets)

        # every <timing> loops increment index to seek the next target in the list
        count = count+1
        index = count%timing

    else:

        rc.ForwardM1(address,0)
        rc.ForwardM2(address,0)

def SeekNext(t):

    # Get speeds and currents
    (a,cur1,cur2) = rc.ReadCurrents(address)y
    w1 = rc.ReadSpeedM1(address)
    w2 = rc.ReadSpeedM2(address)

    if(a):
        # Find increments to PWM
        thisError1 = target1-cur1
        increment1 = _kp*(thisError1)+_kd*(thisError1-lastError1)+_kw*(w1)

        thisError2 = target2-cur2
        increment2 = _kp*(thisError2)+_kd*(thisError2-lastError2)+_kw*(w2)

        # Update errors
        lastError1 = thisError1
        lastError2 = thisError2

    PWM1 = PWM1 + increment1
    PWM2 = PWM2 + increment2
    if PWM1 > 255:
        PWM1 = 255
    if PWM1 < -255:
        PWM1 = -255
    if PWM2 > 255:
        PWM2 = 255
    if PWM2 < -255:
        PWM2 = -255
    if PWM1 >= 0:
        rc.ForwardM1(address,PWM1)
    else:
        rc.BackwardM1(address,-PWM1)
    if PWM2 >= 0:
        rc.ForwardM2(address,PWM2)
    else:
        rc.BackwardM2(address,-PWM2)
=======
# EXECUTED WHILE FALLING


def preppingForFall():

	"""preppingForFall: 

	Arguments:
	(none)
	"""

	# read sensors
	# wait for position to be ready, give continuous feedback
	# alert when ready --> interface with some warning sign on Pi
	# flip safety --> input y

def duringFall():

	"""duringFall: 

	Arguments:
	(none)
	"""

	# read sensors/encoders
	# read current/torque values --> save to array

	# start in caution mode
	# if velocity profile exceeds value, start applying torques from torque list

def torqueControl():

	"""torqueControl: 

	Arguments:
	(none)
	"""

	return data


def readSensors():
	"""readSensors: 

	Arguments:
	(none)
	"""

	# read pins from gpio
	# read encoder values from motor

	pass
>>>>>>> Stashed changes
