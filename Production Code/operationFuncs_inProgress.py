import roboclaw as rc
import RPi.GPIO as GPIO
import config



GPIO.setup(config.gpioPin, GPIO.IN)




# undeclared variables:
#accel
#speed
#decel



def set_motors():
    # implement way to get feedback on position for this
    # write ascii animation to help move joints into position
    position_Knee, position_Hip = mapAngleToPulse(config.initialAngle_Knee, config.initialAngle_Hip)
    time.sleep(1)
    rc.SpeedAccelDeccelPositionM1(config.address, accel, speed, decel, position_Knee, 0)
    rc.SpeedAccelDeccelPositionM2(config.address, accel, speed, decel, position_Hip, 0)
    time.sleep(1.5)
    print('Knee Angle set to {}'.format(config.initialAngle_Knee))
    print('Hip Angle set to {}'.format(config.initialAngle_Hip))


# NEEDS WORK
def getPulseFromAngle(angleKnee, angleHip):
    position_Knee = config.calibratedValues[0]-angleKnee * config.pulsePerRotation/np.pi
    position_Hip = config.calibratedValues[1]-angleHip * config.pulsePerRotation/np.pi
    return position_Knee, position_Hip


# MAYBE GOOD?
def getAngleFromPulse(pulseKnee, pulseHip):
    angleKnee = ((pulseKnee - config.calibratedValues[0]) % config.pulsePerRotation) * np.pi/config.pulsePerRotation
    angleHip = ((pulseHip - config.calibratedValues[1]) % config.pulsePerRotation) * np.pi/config.pulsePerRotation
    return angleKnee, angleHip


# 768(=12*64) pulses per rotation
# operate on ring mod 768












import readline,thread
import sys,struct,fcntl,termios

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



