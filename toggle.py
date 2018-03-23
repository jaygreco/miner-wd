import RPi.GPIO as GPIO

#toggles gpio pin from INPUT (high-z) to OUTPUT_LOW
def toggle_GPIO(pin):
	#switch the gpio from input to output
	GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

	#wait, set high again
	time.sleep(2)
	GPIO.output(pin, GPIO.HIGH)

	#switch the gpio back to input
	GPIO.setup(pin, GPIO.IN)
	GPIO.cleanup() 
	return

if __name__ == '__main__':
	GPIO.setmode(GPIO.BOARD)
	toggle_GPIO(37)