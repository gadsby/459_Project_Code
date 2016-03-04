import roboclaw as rc
import instructions
import time
import RPi.GPIO as GPIO
import serial
import data
import threading
from config import *

# undeclared variables:
#address

GPIO.setup(18, GPIO.IN)
rc.Open("COM5", 115200)


def killMotors():
    rc.ForwardM1(address,0)
    rc.ForwardM2(address,0)


# undeclared variables:
#angle1
#angle2
#accel
#speed
#decel

def set_motors():
    print('\nSetting motors to initial position \n')
    position1, position2 = mapAngleToPulse(angle1, angle2)
    time.sleep(1)
    rc.SpeedAccelDeccelPositionM2(address,accel,speed,decel,position1,0)
    rc.SpeedAccelDeccelPositionM2(address,accel,speed,decel,position2,0)
    time.sleep(1.5)
    print('Motors set to ('+angle1+','+angle2+')'+' degrees \n')


# undeclared variables:
#pulse_per_deg
#ref # global; already dealt with

def mapAngleToPulse(angle1,angle2):
    position1 = ref[0]-angle1*pulse_per_deg
    position2 = ref[1]-angle2*pulse_per_deg
    return position1, position2


# undeclared variables:
#targetsList
#kp
#kd
#kw
#timing
#numberOfTargets




# fix instructions and event timing for falling program

def falling():

    print('\nFALLING: Here I go falling!')

    timeStart = time.clock()
    count, index, lastError1, lastError2, pwm1, pwm2 = [0]*6

    # define numpy array of appropriate size

    while time.clock() - timeStart < 0.8:
        target1,target2 = targetsList(index)
        readSuccessful, current1, current2 = rc.ReadCurrents(address)
        w1 = rc.ReadSpeedM1(address)
        w2 = rc.ReadSpeedM2(address)

    # TODO: Save all fields collected during control loop

    # save angles into array

        if readSuccessful:
            # Find increments to PWM
            thisError1, thisError2 = target1-current1, target2-current2
            increment1, increment2 = kp*thisError1+kd*(thisError1-lastError1)+kw*w1, kp*thisError2+kd*(thisError2-lastError2)+kw*w2

            # Update errors
            lastError1, lastError2 = thisError1, thisError2
            pwm1, pwm2 = pwm1+increment1, pwm2+increment2
            pwm1, pwm2 = min(abs(pwm1), 255) * pwm1/abs(pwm1), min(abs(pwm2), 255) * pwm2/abs(pwm2)

        if pwm1 >= 0:
            rc.ForwardM1(address,pwm1)
        else:
            rc.BackwardM1(address,-pwm1)

        if pwm1 >= 0:
            rc.ForwardM2(address,pwm2)
        else:
            rc.BackwardM2(address,-pwm2)

        count += 1
        index = count % timing

        if index > numberOfTargets:
            index = numberOfTargets
        else:
            killMotors()

    return [0]*5 # data output here

