import RPi.GPIO
import time
import thread


brightness = 0.0

def setBrightnessThread():
	global brightness
	while True:
		brightness = 1.0
		#print("brightness=%d" %(brightness))
		time.sleep(1)

		brightness = 7.0
		#print("brightness=%d" %(brightness))
		time.sleep(1)
	
		brightness = 24.0
		#print("brightness=%d" %(brightness))
		time.sleep(1)



def brightnessWorker():
	global brightness

	count = 0
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
		# turn on outputs for brief time
		RPi.GPIO.output(2, True)
		RPi.GPIO.output(3, True)
		RPi.GPIO.output(4, True)
		RPi.GPIO.output(17, True)
		RPi.GPIO.output(27, True)
		time.sleep(brightness/1000)

		# turn off outputs for remaining part of time.
		RPi.GPIO.output(2, False)
		RPi.GPIO.output(3, False)
		RPi.GPIO.output(4, False)
		RPi.GPIO.output(17, False)
		RPi.GPIO.output(27, False)
		time.sleep((25-brightness)/1000)

		count = count + 1;
		if count == 40:
			count=0
			#print("worker brightness = %d" % (brightness))
			

try:
	thread.start_new_thread( setBrightnessThread, () )
except:
	print "Error: unable to start thread"


try:
	thread.start_new_thread( brightnessWorker, () )
except:
	print "Error: unable to start thread"

while True:
	time.sleep(1)


