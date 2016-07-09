import RPi.GPIO
import time
import thread
import random
import pygame
import argparse
import threading


parser=argparse.ArgumentParser(description='Create creepy scene with randomly blinking eyes.')
parser.add_argument('-s', '--sound', action='store_true', help='Enable Sound output')
args = parser.parse_args()

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setwarnings(False)


try:
	if (args.sound):
		pygame.mixer.init()
		pygame.mixer.music.load("eerie-forest.mp3")
		pygame.mixer.music.play()
		owlHoot       = pygame.mixer.Sound("owlhoot-clean.wav")
		largeWolfHowl = pygame.mixer.Sound("large-wolf-howl.wav")
		wolf_1        = pygame.mixer.Sound("wolf_1.wav")
		clownlaugh    = pygame.mixer.Sound("clown-laugh.wav")
	else:
		owlHoot       = None
		largeWolfHowl = None
		wolf_1        = None
		clownlaugh    = None


	brightness = [0.0, 0.0, 0.0, 0.0, 0.0]   # brightness levels 0=off;  25=on full brightness
	gpioNumber = [2,3,4,17,27]    # physical gpio numbers
	rightToLeft = [3,4,0,1,2]    # order of logical outputs in desired order
	waitEvents = []
	waitEventsDone = []
	for index in xrange(5):
		RPi.GPIO.setup(gpioNumber[index], RPi.GPIO.OUT)
		RPi.GPIO.output(gpioNumber[index], False)
		waitEvents.append(threading.Event() )
		waitEventsDone.append(threading.Event() )

	def playSound(soundObject,minDelay, maxDelay ):
		while True:
			if (args.sound):
				playChannel = soundObject.play()
				while playChannel.get_busy() == True:
					time.sleep(0.25)
			#print("completed owl sound")
			time.sleep(random.randint(minDelay,maxDelay))


	def handleBlinkSequence(gpioIndex):
		brightness[gpioIndex] = 25.0
		time.sleep(.033)

		brightness[gpioIndex] = 20.0
		time.sleep(.033*1)  # blink pose 2

		brightness[gpioIndex] = 0.0
		time.sleep(.033*2)  # blink pose 3,4

		brightness[gpioIndex] = 2.0
		time.sleep(.033*1)  # blink pose 5

		brightness[gpioIndex] = 10.0
		time.sleep(.033*1)  # blink pose 6

		brightness[gpioIndex] = 25.0

	def waitTillAllComplete():
		for index in xrange(5):
			waitEventsDone[index].wait();
			waitEventsDone[index].clear();

	def setBrightnessThread(name, gpioIndex, soundObject=None, minDelay=5, maxDelay=25 ):
		global brightness
		while True:
			waitEvents[gpioIndex].wait()   # wait till we are told to blink.
			waitEvents[gpioIndex].clear()
			
			if ( not soundObject == None ):
				playChannel = soundObject.play()

			handleBlinkSequence(gpioIndex)

			if ( not soundObject == None ):
				while playChannel.get_busy() == True:
					time.sleep(0.25)

#			time.sleep(random.randint(minDelay,maxDelay))
			waitEventsDone[gpioIndex].set();   #signal that we are done.



	def masterControlThread():
		while True:
			sequenceBlinkRightToLeft()
			time.sleep(1)
			sequenceBlinkLeftToRight()
			time.sleep(1)
			sequenceBlinkAllBlink()
#			time.sleep(1)
			sequenceBlinkAllBlink()
			time.sleep(1)
		
	def sequenceBlinkUp():
		for index in xrange(5):
			waitEvents[index].set()
			time.sleep(0.25)
		waitTillAllComplete()
			
	def sequenceBlinkDown():
		for index in xrange(5):
			waitEvents[4-index].set()
			time.sleep(0.25)
		waitTillAllComplete()
		
	def sequenceBlinkAllBlink():
		for index in xrange(5):
			waitEvents[4-index].set()
		waitTillAllComplete()
		
	def sequenceBlinkRightToLeft():
		for tempindex in xrange(5):
			index = rightToLeft[tempindex]
			waitEvents[index].set()
			time.sleep(0.25)
		waitTillAllComplete()

	def sequenceBlinkLeftToRight():
		for tempindex in xrange(5):
			index = rightToLeft[4-tempindex]
			waitEvents[index].set()
			time.sleep(0.25)
		waitTillAllComplete()




	def brightnessWorker(name, gpioIndex):
		global brightness
		global gpioNumber

		#print "starting %s on gpioNumber[%d] = %d" % (name, gpioIndex, gpioNumber[gpioIndex] )



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
		thread.start_new_thread( setBrightnessThread, ("owl",       0, owlHoot      , 5,  30) )
		thread.start_new_thread( setBrightnessThread, ("small owl", 1, owlHoot      , 5,  30) )
		thread.start_new_thread( setBrightnessThread, ("bear",      2, wolf_1       , 10,  30) )
		thread.start_new_thread( setBrightnessThread, ("troll",     3, clownlaugh   , 10,  30) )
		thread.start_new_thread( setBrightnessThread, ("tv spider", 4, largeWolfHowl, 10,  30) )
	except:
		print "Error: unable to start setBrightnessThread thread"


	try:
		thread.start_new_thread( brightnessWorker, ("owl", 0 ) )
		thread.start_new_thread( brightnessWorker, ("small owl", 1) )
		thread.start_new_thread( brightnessWorker, ("bear", 2) )
		thread.start_new_thread( brightnessWorker, ("troll", 3) )
		thread.start_new_thread( brightnessWorker, ("tv spider", 4) )
	except:
		print "Error: unable to start thread"

	try:
	 	thread.start_new_thread( masterControlThread() )
	except:
		print "Error: unable to start masterControlThread thread"

	while True:
		if (args.sound):
			pygame.mixer.music.play()
			while pygame.mixer.music.get_busy() == True:
				time.sleep(0.25)
			print("completed sound")
		else:
			time.sleep(1)

finally:
	for gpio in gpioNumber:
		waitEvents[index].set()
		RPi.GPIO.output(gpio, False)

