#!/usr/bin/python

# Import required Python libraries
import time
import RPi.GPIO as GPIO
import subprocess

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO    = 24
GPIO_MODE    = 27
GPIO_BOUTON  = 22 

PROXIMITE = 100 # distance a laquelle on declenche la lecture
DELAI = 1 # delai avant que la lecture ne commence

def mesure():
	# Send 10us pulse to trigger
	GPIO.output(GPIO_TRIGGER, True)
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)
	#start = time.time()
	while GPIO.input(GPIO_ECHO)==0:
		start = time.time()
	while GPIO.input(GPIO_ECHO)==1:
		stop = time.time()
	# Calculate pulse length
	elapsed = stop-start
	# Distance pulse travelled in that time is time
	# multiplied by the speed of sound (cm/s)
	distance = elapsed * 34300
	# That was the distance there and back so halve the value
	return distance / 2

def play():
	# call(["./play.sh"])
	process = subprocess.Popen("./play.sh", shell=True)
	while process.poll() is None:
		if GPIO.event_detected(GPIO_BOUTON):
			print "STOP"
			GPIO.remove_event_detect(GPIO_BOUTON)
			subprocess.call(["./stop.sh"], shell=True)
			time.sleep(1)
			GPIO.add_event_detect(GPIO_BOUTON, GPIO.RISING, bouncetime=300)
			
def init():
	# Use BCM GPIO references
	# instead of physical pin numbers
	GPIO.setmode(GPIO.BCM)
	# Set pins as output and input
	GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
	GPIO.setup(GPIO_ECHO,GPIO.IN)
	GPIO.setup(GPIO_MODE,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(GPIO_BOUTON,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
	# Set trigger to False (Low)
	GPIO.output(GPIO_TRIGGER, False)
	# Allow module to settle
	time.sleep(1)
	# declenchement de la lecture
	GPIO.add_event_detect(GPIO_BOUTON, GPIO.RISING, bouncetime=300)

def loop():
	print "PRET"
	presence = time.time()
	while True:
		if GPIO.input(GPIO_MODE) == GPIO.HIGH:
			print "PRESSION"
			# declenchement par pression
			if GPIO.event_detected(GPIO_BOUTON):
					print "PLAY"
					play()
		else:
			print "DISTANCE"
			# declenchement par presence
			distance = mesure()
			print "distance: %d cm" %(distance)
			
			# declenchement par pression
			if GPIO.event_detected(GPIO_BOUTON):
					print "PLAY"
					play()
			else:
				if distance > PROXIMITE:
					presence = time.time()
				else:
					if time.time() - presence > DELAI:
						print "PLAY"
						play()
						presence = time.time()
					else:
						print "DELAI PRESENCE"
		# attendre une seconde avant de tester a nouveau
		time.sleep(0.5)

if __name__ == "__main__":
	init()
	loop()
	GPIO.cleanup()