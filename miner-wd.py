import requests
import time
import RPi.GPIO as GPIO

#list of workers to watch
#can be a single worker
workers = ['k2s0', 'fakeworker']

#function definitions
#wait function, in hours
def wait(hours):
	time.sleep(minutes*3600)
	return

#nonlinear timeout (0.5h, 2h, 1d thereafter)
def nonlinear_timeout():
	#timeout stages in hours
	#this can be changed to any set of intervals
	timeouts = [0.5, 2, 24]

	#read state of timeout counter
	if timeout_counter >= len(timeouts):
		#wait the longest timeout
		wait(timeouts[-1])
	else:
		#wait the correct timer
		wait(timeouts[timeout_counter])

	#increment the timeout counter
	timeout_counter += 1;

	return

#resets the timeout counter back to 30m
def reset_timeout():
	timeout_counter = 0
	return

#checks that all workers passed in workers[] are active.
#if the workers are not active, a warning is printed and the function returns False
#returns True if everything is OK
#NH: 31sJYXu9r6gsHZeTLKNRaBpkoSmc7r7WVC
def check_NH_workers(addr, workers):
	#use nicehash api to gather info regarding workers
	payload = {'method': 'stats.provider.workers', 'addr': addr}
	r = requests.get('http://api.nicehash.com/api', params=payload)

	try:
		j = r.json()
		for worker in workers:
			#if worker is not in worker list, return false
                        if not any(worker in sl for sl in j['result']['workers']):
                        #if worker not in j['result']['workers']:
				print worker, 'not in worker list!'
				print j['result']['workers']
                                return False
	except:
		#there was an API issue or otherwise
		pass

	#if we made it this far, assume all is OK
	return True

#toggles gpio pin from INPUT (high-z) to OUTPUT_LOW
def toggle_GPIO(pin):
	#switch the gpio from input to output
	GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

	#wait, set high again
	time.sleep(2)
	GPIO.output(pin, GPIO.HIGH)

	#switch the gpio back to input
	GPIO.setup(pin, GPIO.IN)
	return

#reset wrapper function
#intended for use with output pin 37 (IO) and 39 (GND)
def reset_rig():
	toggle_GPIO(37)
	return

#main
if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    timeout_counter = 0
    while True:
    	#check status
    	if not check_NH_workers('31sJYXu9r6gsHZeTLKNRaBpkoSmc7r7WVC', workers):
	    	#there is an issue
	    	print "Issue with workers! Resetting..."
	    	#reset_rig()
	    	nonlinear_timeout()
    	else:
    		reset_timeout()
			
    	#wait before checking again
    	wait(0.5)			
