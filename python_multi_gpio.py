import RPi.GPIO
import time
import thread


brightness = 0.0
gpioNumber = [2,3,4,17,27]

RPi.GPIO.setmode(RPi.GPIO.BCM)

def setBrightnessThread():
	global brightness
	while True:
		brightness = 25.0
		time.sleep(1)

		brightness = 20.0
		time.sleep(.033*1)  # blink pose 2
	
		brightness = 0.0
		time.sleep(.033*2)  # blink pose 3,4
	
		brightness = 2.0
		time.sleep(.033*1)  # blink pose 5
	
		brightness = 10.0
		time.sleep(.033*1)  # blink pose 6
	





		brightness = 25.0
		time.sleep(1)




		brightness = 0.0
		time.sleep(.033*6)  # blink pose 3,4

		brightness = 25.0
		time.sleep(1)





def brightnessWorker(name, gpioIndex):
	global brightness
	global gpioNumber

	print "starting %s on gpioNumber[%d] = %d" % (name, gpioIndex, gpioNumber[gpioIndex] )

	RPi.GPIO.setup(gpioNumber[gpioIndex], RPi.GPIO.OUT)

	RPi.GPIO.output(gpioNumber[gpioIndex], False)

	while True:
		# turn on outputs for brief time
		if brightness != 0:
			RPi.GPIO.output(gpioNumber[gpioIndex], True)
			time.sleep(brightness/1000)

		# turn off outputs for remaining part of time.
		if brightness != 25:
			RPi.GPIO.output(gpioNumber[gpioIndex], False)
			time.sleep((25-brightness)/1000)


			

try:
	thread.start_new_thread( setBrightnessThread, () )
except:
	print "Error: unable to start setBrightnessThread thread"


try:
	thread.start_new_thread( brightnessWorker, ("owl", 0) )
	thread.start_new_thread( brightnessWorker, ("leftbook", 1) )
	thread.start_new_thread( brightnessWorker, ("bear", 2) )
	thread.start_new_thread( brightnessWorker, ("troll", 3) )
	thread.start_new_thread( brightnessWorker, ("tv spider", 4) )
except:
	print "Error: unable to start thread"

while True:
	time.sleep(1)


