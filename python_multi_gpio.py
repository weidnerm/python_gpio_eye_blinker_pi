import RPi.GPIO
import time
import thread
import random
import pygame

pygame.mixer.init()
pygame.mixer.music.load("eerie-forest.mp3")
pygame.mixer.music.play()
owlHoot = pygame.mixer.Sound("owlhoot-clean.wav")


brightness = [0.0, 0.0, 0.0, 0.0, 0.0] 
gpioNumber = [2,3,4,17,27]

RPi.GPIO.setmode(RPi.GPIO.BCM)

def playOwlHoots(name, dummy):
	while True:
		global owlHoot
		owlPlayChannel = owlHoot.play()
		while owlPlayChannel.get_busy() == True:
			time.sleep(0.25)
		#print("completed owl sound")
		time.sleep(random.randint(5,10))
	

def setBrightnessThread(name, gpioIndex):
	global brightness
	while True:
		brightness[gpioIndex] = 25.0
		time.sleep(1)

		brightness[gpioIndex] = 20.0
		time.sleep(.033*1)  # blink pose 2
	
		brightness[gpioIndex] = 0.0
		time.sleep(.033*2)  # blink pose 3,4
	
		brightness[gpioIndex] = 2.0
		time.sleep(.033*1)  # blink pose 5
	
		brightness[gpioIndex] = 10.0
		time.sleep(.033*1)  # blink pose 6
	





		brightness[gpioIndex] = 25.0
		time.sleep(random.randint(2,10))









def brightnessWorker(name, gpioIndex):
	global brightness
	global gpioNumber

	#print "starting %s on gpioNumber[%d] = %d" % (name, gpioIndex, gpioNumber[gpioIndex] )

	RPi.GPIO.setup(gpioNumber[gpioIndex], RPi.GPIO.OUT)

	RPi.GPIO.output(gpioNumber[gpioIndex], False)

	while True:
		# turn on outputs for brief time
		if brightness[gpioIndex] != 0:
			RPi.GPIO.output(gpioNumber[gpioIndex], True)
			time.sleep(brightness[gpioIndex]/1000)

		# turn off outputs for remaining part of time.
		if brightness[gpioIndex] != 25:
			RPi.GPIO.output(gpioNumber[gpioIndex], False)
			time.sleep((25-brightness[gpioIndex])/1000)


			

try:
	thread.start_new_thread( setBrightnessThread, ("owl", 0) )
	thread.start_new_thread( setBrightnessThread, ("leftbook", 1) )
	thread.start_new_thread( setBrightnessThread, ("bear", 2) )
	thread.start_new_thread( setBrightnessThread, ("troll", 3) )
	thread.start_new_thread( setBrightnessThread, ("tv spider", 4) )
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

try:
	thread.start_new_thread( playOwlHoots, ("owl", 0) )

except:
	print "Error: unable to start sound thread"


while True:
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
		time.sleep(0.25)
	print("completed sound")


