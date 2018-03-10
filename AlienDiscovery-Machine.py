#!/usr/bin/env python
import redis
import ADC0832
import time
import RPi.GPIO as GPIO

r = redis.Redis(host='redis-18803.c11.us-east-1-2.ec2.cloud.redislabs.com', port='18803', password='#############')

##Setup for LED GPIO ##
GPIO.setmode(GPIO.BOARD)       # Numbers pins by physical location
GPIO.setup(15, GPIO.OUT)       # Set pin mode as output
GPIO.output(15, GPIO.HIGH)     # Set pin to high(+3.3V) to off the led

##Setup for Buzzer GPIO ##
BeepPin = 37    # pin11
GPIO.setup(BeepPin, GPIO.OUT)   # Set pin mode as output
GPIO.output(BeepPin, GPIO.LOW) # Set pin to high(+3.3V) to off the beep


##Setup for Ultrasonic GPIO ##
GPIO.setup(16,GPIO.OUT,initial=GPIO.LOW)        #setup distance sensor for alien trigger
GPIO.setup(18,GPIO.IN)                          #setup distance sensor for alien echo


##Setup for 7-Segment display for GPIO ##
DIO = 29
CLK = 31
STB = 33
LSBFIRST = 0
MSBFIRST = 1
tmp = 0

##Start - Functions for 7-Segment display for GPIO ##
def _shiftOut(dataPin, clockPin, bitOrder, val):
	for i in range(8):
		if bitOrder == LSBFIRST:
			GPIO.output(dataPin, val & (1 << i))
		else:
			GPIO.output(dataPin, val & (1 << (7 -i)))
		GPIO.output(clockPin, True)
		time.sleep(0.000001)			
		GPIO.output(clockPin, False)
		time.sleep(0.000001)			
	
def sendCommand(cmd):
	GPIO.output(STB, False)
	_shiftOut(DIO, CLK, LSBFIRST, cmd)
	GPIO.output(STB, True)

def TM1638_init():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(DIO, GPIO.OUT)
	GPIO.setup(CLK, GPIO.OUT)
	GPIO.setup(STB, GPIO.OUT)
	sendCommand(0x8f)

def numberDisplay(num):
	digits = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f]
	sendCommand(0x40)
	GPIO.output(STB, False)
	_shiftOut(DIO, CLK, LSBFIRST, 0xc0)
	_shiftOut(DIO, CLK, LSBFIRST, digits[num/1000%10])
	_shiftOut(DIO, CLK, LSBFIRST, 0x00)
	_shiftOut(DIO, CLK, LSBFIRST, digits[num/100%10])
	_shiftOut(DIO, CLK, LSBFIRST, 0x00)
	_shiftOut(DIO, CLK, LSBFIRST, digits[num/10%10])
	_shiftOut(DIO, CLK, LSBFIRST, 0x00)
	_shiftOut(DIO, CLK, LSBFIRST, digits[num%10])
	_shiftOut(DIO, CLK, LSBFIRST, 0x00)
	GPIO.output(STB, True)

def numberDisplay_dec(num):
	digits = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f]
	integer = 0
	decimal = 0

	pro = int(num * 100)

	integer = int(pro / 100)
	decimal = int(pro % 100)

	sendCommand(0x40)
	GPIO.output(STB, False)
	_shiftOut(DIO, CLK, LSBFIRST, 0xc0)
	_shiftOut(DIO, CLK, LSBFIRST, digits[integer/10])
	_shiftOut(DIO, CLK, LSBFIRST, 0x00)
	_shiftOut(DIO, CLK, LSBFIRST, digits[integer%10] | 0x80)
	_shiftOut(DIO, CLK, LSBFIRST, 0x00)
	_shiftOut(DIO, CLK, LSBFIRST, digits[decimal/10])
	_shiftOut(DIO, CLK, LSBFIRST, 0x00)
	_shiftOut(DIO, CLK, LSBFIRST, digits[decimal%10])
	_shiftOut(DIO, CLK, LSBFIRST, 0x00)
	GPIO.output(STB, True)
##End - Functions for 7-Segment display for GPIO ##



#function to measure distance for ultrasonic distance sensor
def checkdist():
	GPIO.output(16, GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(16, GPIO.LOW)
	while not GPIO.input(18):
		pass
	t1 = time.time()
	while GPIO.input(18):
		pass
	t2 = time.time()
	return (t2-t1)*340/2


time.sleep(2)


def init():
	ADC0832.setup()

def loop():
        r.set('AlienCounter', "0")
        print "AlienCounter : " + r.get('AlienCounter')
	while True:
		#The ADC0832 has two channels
		#res = ADC0832.getResult()   <-- It reads channel 0 by default. Equivalent to getResult(0)
		#res = ADC0832.getResult(1)  <-- Use this to read the second channel

                currenttime = time.strftime("%d-%b-%Y %H:%M:%S", time.gmtime()) 
                print'Date/Time: ' + currenttime
                r.set('AlienDateTime', currenttime)
		distance = checkdist()
		print 'Distance: %0.2f m' %distance
		res = ADC0832.getResult() - 80
		print 'res = %d' %res
        	numberDisplay_dec(distance)
        	r.set('AlienDistance', distance)
        	r.set('AlienSolar', res)
                #time.sleep(4) # 4s
		if distance < 0.1:
                        print '...led on'
                        GPIO.output(15, GPIO.LOW)       # led on
                        r.set('AlienLED', "ON")
                    	GPIO.output(BeepPin, GPIO.HIGH)  #buzzer on
                    	r.set('AlienBuzzer', "ON")
                    	r.incr('AlienCounter')
                    	print "AlienCounter : " + r.get('AlienCounter')
                        #time.sleep(0.1)
                        #time.sleep(0.5)
		if distance > 0.1:
			print 'led off...'
                        GPIO.output(15, GPIO.HIGH)      # led off
                        r.set('AlienLED', "OFF")
        		GPIO.output(BeepPin, GPIO.LOW) #buzzer off
                    	r.set('AlienBuzzer', "OFF")
                	r.set('AlienCounter', "0")
                    	print "AlienCounter : " + r.get('AlienCounter')
                        #time.sleep(0.1)
                        #time.sleep(0.5)
                        if res < 0:
                                #res = 0
                                print '...led on'
                                GPIO.output(15, GPIO.LOW)  # led on
                            	GPIO.output(BeepPin, GPIO.HIGH)  #buzzer on
                                r.set('AlienLED', "ON")
                            	r.set('AlienBuzzer', "ON")
                            	r.incr('AlienCounter')
                            	print "AlienCounter : " + r.get('AlienCounter')
                                #time.sleep(0.1)
                                #time.sleep(0.5)
                        if res > 100:
                                #res = 100
                                print 'led off...'
                                GPIO.output(15, GPIO.HIGH)      # led off
                		GPIO.output(BeepPin, GPIO.LOW) #buzzer off
                                r.set('AlienLED', "OFF")
                            	r.set('AlienBuzzer', "OFF")
                        	r.set('AlienCounter', "0")
                                print "AlienCounter : " + r.get('AlienCounter')
                                #time.sleep(0.1)
                                #time.sleep(0.5)
		time.sleep(0.5)

if __name__ == '__main__':
	init()
	try:
                TM1638_init()
                GPIO.setup(BeepPin, GPIO.OUT)   # Set pin mode as output
                GPIO.output(BeepPin, GPIO.LOW) # Set pin to high(+3.3V) to off the beep
		loop()
	except KeyboardInterrupt: 
		GPIO.output(15, GPIO.HIGH)     # led off
        	GPIO.output(BeepPin, GPIO.HIGH)    # beep off
                GPIO.cleanup()                 # Release resource
		ADC0832.destroy()
		print 'The end !'
