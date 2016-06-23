import RPi.GPIO
import time


try:
	RPi.GPIO.setmode(RPi.GPIO.BCM)
	
	# pin 11 is GPIO17
	RPi.GPIO.setup(2, RPi.GPIO.OUT)
	RPi.GPIO.setup(3, RPi.GPIO.OUT)
	RPi.GPIO.setup(4, RPi.GPIO.OUT)
	RPi.GPIO.setup(17, RPi.GPIO.OUT)
	RPi.GPIO.setup(27, RPi.GPIO.OUT)

	RPi.GPIO.output(2, False)
	RPi.GPIO.output(3, False)
	RPi.GPIO.output(4, False)
	RPi.GPIO.output(17, False)
	RPi.GPIO.output(27, False)

	while True:
		RPi.GPIO.output(2, True)
		time.sleep(1)
		RPi.GPIO.output(2, False)
		time.sleep(1)
	
		RPi.GPIO.output(3, True)
		time.sleep(1)
		RPi.GPIO.output(3, False)
		time.sleep(1)
	
		RPi.GPIO.output(4, True)
		time.sleep(1)
		RPi.GPIO.output(4, False)
		time.sleep(1)
	
		RPi.GPIO.output(17, True)
		time.sleep(1)
		RPi.GPIO.output(17, False)
		time.sleep(1)
	
		RPi.GPIO.output(27, True)
		time.sleep(1)
		RPi.GPIO.output(27, False)
		time.sleep(1)

finally:  
	RPi.GPIO.setup(2, RPi.GPIO.IN)
	RPi.GPIO.setup(3, RPi.GPIO.IN)
	RPi.GPIO.setup(4, RPi.GPIO.IN)
	RPi.GPIO.setup(17, RPi.GPIO.IN)
	RPi.GPIO.setup(27, RPi.GPIO.IN)
	RPi.GPIO.cleanup() # this ensures a clean exit 


