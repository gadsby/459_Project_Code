import roboclaw as rc
import instructions
import time
import RPi.GPIO as GPIO
import serial
import data
import threading
from config import *

GPIO.setup(18, GPIO.IN)
rc.Open("COM5", 115200)
rc.ForwardM1(address,0)
rc.ForwardM2(address,0)

# needs improvement to structure, consistency, and documentation, but state transitions work

# TODO:
# 1) Fill in functions with actual control and data collection


def falling():

    print('')
    print('FALLING: Here I go falling!')

    beginning = time.clock()

    count = 0
    index = 0
    lastError1 = 0
    lastError2 = 0
    pwm1 = 0
    pwm2 = 0

    while time.clock() - beginning < 0.8:
        target1,target2 = targetsList(index)
        (a,cur1,cur2) = rc.ReadCurrents(address)
        w1 = rc.ReadSpeedM1(address)
        w2 = rc.ReadSpeedM2(address)

    # TODO: Save all fields collected during control loop

        if(a):
            # Find increments to PWM
            thisError1 = target1-cur1
            increment1 = kp*thisError1+kd*(thisError1-lastError1)+kw*w1

            thisError2 = target2-cur2
            increment2 = kp*thisError2+kd*(thisError2-lastError2)+kw*w2

            # Update errors

            lastError1 = thisError1
            lastError2 = thisError2

            pwm1 =+ increment1
            pwm2 =+ increment2


        if pwm1 > 255:
            pwm1 = 255
        if pwm1 < -255:
            pwm1 = -255
        if pwm2 > 255:
            pwm2 = 255
        if pwm2 < -255:
            pwm2 = -255
        if pwm1 >= 0:
            rc.ForwardM1(address,pwm1)
        else:
            rc.BackwardM1(address,-pwm1)
        if pwm2 >= 0:
            rc.ForwardM2(address,pwm2)
        else:
            rc.BackwardM2(address,-pwm2)

        count =+ 1
        index = count%timing
        if index > numberOfTargets:
            index = numberOfTargets
        else:
            rc.ForwardM1(address,0)
            rc.ForwardM2(address,0)

    return [0]*5


class CondChecker (threading.Thread):
    def __init__(self,primed):
        threading.Thread.__init__(self,primed)
        self.primed = primed

    def stop(self):
        primed = False

    def run(self):
        primed = True
        while primed == True:
            #Read Potentiometer Values
            w = GPIO.read
            x = GPIO.read
            y = GPIO.read
            if y>x>w:
                falling()




# ref will be valueless until zeroing function has been run
def f(angle1,angle2):
    position1 = ref[0]-angle1*pulse_per_deg
    position2 = ref[1]-angle2*pulse_per_deg

    return position1,position2

# TODO: put back to Main Menu option (DONE)
# TODO: improve Main Menu option

def set_motors():
    print('')
    print 'Setting motors to initial position \n'
    position1,position2 = f(angle1,angle2)
    time.sleep(1000)
    rc.SpeedAccelDeccelPositionM2(address,accel,speed,deccel,position1,0)
    rc.SpeedAccelDeccelPositionM2(address,accel,speed,deccel,position2,0)
    time.sleep(1500)
    print 'Motors set to ('+angle1+','+angle2+')'+' degrees \n'


def push_into_position_func():

    set_motors()

    while True:
        var = input('Options: N (Neutral) / P (Primed) / M (Main Menu)\n')
        if var == 'N':
            return 0
        elif var == 'P':
            return 1
        elif var == 'M':
            return 9
        else:
            print('Invalid. Choose \'N\', \'P\', or \'M\'.\n')



# TODO: put switch to neutral option (DONE)
def primed_state():
    print ('')
    print ('PRIMED: Apparatus is primed and awaiting fall conditions to be met.')
    checker = CondChecker(True)
    checker.run()

    while True:
        var = input('Press \'N\'to return to neutral state.')
        print
        if var == 'N':
            checker.stop()
            return 'N'



# TODO: put switch options for main menu and push_into_position_func (DONE)
def neutral_state():
    print('')
    rc.ForwardM1(address,0)
    rc.ForwardM2(address,0)
    print('NEUTRAL: Apparatus is set to neutral and awaiting feedback to transition to primed state.')
    print('Press \'M\' to go to the main menu, or \'R\' to restart falling scheme.')
    var = input('Press any other key and <ENTER> to move into primed state.\n')
    if var == 'M':
        return 9
    elif var == 'R':
        return 8
    else:
        return 0



def save_data(data):
    print('')
    print('SAVING: And here I go saving some data (not actually saving data).')
    print('Fake Data: {}'.format(data))
    return






def initiateFallMode():
	while True:
		nextStep = push_into_position_func()

		back2Start = False

		# give option to go to neutral, primed, or quit
		if nextStep == 0: # stay in neutral state
			varNeutral = neutral_state()
			if varNeutral == 8:
				continue
			elif varNeutral == 9:
				return

		elif nextStep == 9: # quit back to Main Menu
			return

		while True:
			if primed_state() == 'N':
				varNeutral = neutral_state()
				if varNeutral == 8:
					back2Start = True
					break
				elif varNeutral == 9:
					return
			else:
				break

		if back2Start:
			continue

		data = falling()
		save_data(data)
		return

