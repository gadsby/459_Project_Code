import time
import RPi.GPIO as GPIO

potentiometer_adc = 0
SPICLK  = 0x12  #18
SPIMOSI = 0x18  #24
SPIMISO = 0x17  #23
SPICS   = 0x19  #25

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)


def readadc(adcnum, clockpin, mosipin, misopin, cspin):

    GPIO.output(cspin, True)
    GPIO.output(clockpin, False)
    GPIO.output(cspin, False)
 
    commandout = (adcnum | 0x18) << 3

    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
 
    adcout = 0
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if (GPIO.input(misopin)):
            adcout |= 0x1

    GPIO.output(cspin, True)
     
    return adcout >> 1      # first bit is 'null' so drop it




if __name__ == '__main__':

    for i in range(100):
        start = time.clock()
        res = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
        stop = time.clock()
        print('PotOutput: {}\tTimeDelay: {}'.format(res, stop-start))
        time.sleep(0.2)
    GPIO.cleanup()


