import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 1

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)
 
        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low
 
        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
 
        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1
 
        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

def zero_pot():
        """ zeros current position of potentiometer     """
        zero_pos = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
        return zero_pos

# SPI port on the ADC
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

potentiometer_adc = 0

angle_of_rot = 300
adc_max = 1024.0

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

numReadings = 50

readings = [0] * numReadings
readIndex = 0
total = 0
average = 0

zero = zero_pot()
while True:
        #Subtract last reading:
        total = total - readings[readIndex]
        
        adc = zero - readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
        angle = (adc/adc_max)*angle_of_rot

        #read from sensor
        readings[readIndex] = angle

        #add the reading to the total
        total = total + readings[readIndex]

        #advance to the next position in the array
        readIndex = readIndex + 1

        if readIndex >= numReadings:
                readIndex = 0;

        average = total/numReadings

        print ("Angle: %1.3f" % angle)