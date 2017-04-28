### IMPORTANT. DO NOT PROCEED WITHOUT READING. ###
### DO NOT TOUCH THE CODE UNLESS AUTHORIZED. IF YOU ARE MAKING ANY CHANGES, COMMENT THE CHANGELOG BELOW
# This code is for the Microprocessors project by Group 41.
# It involves manually controlling the robot through bluetooth.

import RPi.GPIO as gpio
## We need to import RPi.GPIO library to access the GPIO pins on the Pi.
import bluetooth as bt
## Documentation for this library at - http://htmlpreview.github.io/?https://github.com/karulis/pybluez/blob/master/docs/index.html
import time

def setup(lu_pinno,ll_pinno,ru_pinno,rl_pinno,vac_pinno):
	## setup is basically initializing the pins on the Raspberry Pi
	## We want to tell the Pi that we are using so and so(the pins referred to by lu_pinno,etc.)

	global left_upper,left_lower,right_upper,right_lower,vacuum_pin
	## left_upper,left_lower,right_upper,right_lower correspond to the pins on L293D motor driver.
	## In this pic http://www.rakeshmondal.info/pik/l293d%20pin%20diagram.png ,
	## left_upper = 2,left_lower = 7,right_upper = 15,right_lower = 10
	## As you can see, the variables are named according to the location of the pins on the motor driver. 
	left_upper=lu_pinno
	left_lower=ll_pinno
	right_upper=ru_pinno
	right_lower=rl_pinno
	vacuum_pin = vac_pinno

	gpio.setmode(gpio.BOARD)
	## gpio.setmode tells the Pi what kind of numbering system to use.
	## See here for more info -- https://raspberrypi.stackexchange.com/a/12967
	gpio.setup(left_upper,gpio.OUT)
	## gpio.setup is the main library function which sets up i.e. initializes the pins.
	## gpio.OUT means telling the Pi we want that pin as OUTPUT.
	gpio.setup(left_lower,gpio.OUT)
	gpio.setup(right_upper,gpio.OUT)
	gpio.setup(right_lower,gpio.OUT)
	gpio.setup(vacuum_pin,gpio.OUT)

	# SET ALL PINS TO LOW FIRST
	gpio.output(left_upper,gpio.LOW)
	## gpio.output is telling the Pi what kind of output we want on that pin.
	## gpio.output(left_upper,gpio.LOW) means a digital LOW output on left_upper GPIO pin.
	gpio.output(left_lower,gpio.LOW)
	gpio.output(right_upper,gpio.LOW)
	gpio.output(right_lower,gpio.LOW)
	gpio.output(vacuum_pin,gpio.LOW)

	return

def bind_and_listen(sock):

	port = 1
	sock.bind(("",port))
	## BLuetooth communication happens through end-points called sockets.
	## We need to bind the BT socket to a specific port.
	## sock.bind(("",1)) binds the Bluetooth connection socket to Port 1.
	print 'The RasPi is now listening to you.'
	blinky(indicator_pin,3,0.2)

	sock.listen(1)
	## With listen(1), the socket is now ready to receive incoming connections.

	accept_sock,accept_addr = sock.accept()
	## Return the socket 'object' from this function
	return accept_sock

def receive_data(accepted_sock):
	## Pass the socket 'object' from the previous step.
	data = accepted_sock.recv(1024)
	## Receive upto 1024 bytes
	return data

def move_forward():
	## see the working of L293D to understand these functions.
	global left_upper,left_lower,right_upper,right_lower
	gpio.output(left_upper,gpio.HIGH)
	gpio.output(left_lower,gpio.LOW)
	gpio.output(right_upper,gpio.HIGH)
	gpio.output(right_lower,gpio.LOW)
	return

def move_backward():
	
	global left_upper,left_lower,right_upper,right_lower
	gpio.output(left_upper,gpio.LOW)
	gpio.output(left_lower,gpio.HIGH)
	gpio.output(right_upper,gpio.LOW)
	gpio.output(right_lower,gpio.HIGH)
	return 

def move_right():
	
	global left_upper,left_lower,right_upper,right_lower
	gpio.output(left_upper,gpio.HIGH)
	gpio.output(left_lower,gpio.LOW)
	gpio.output(right_upper,gpio.LOW)
	gpio.output(right_lower,gpio.LOW)
	return

def move_left():
	
	global left_upper,left_lower,right_upper,right_lower
	gpio.output(left_upper,gpio.LOW)
	gpio.output(left_lower,gpio.LOW)
	gpio.output(right_upper,gpio.HIGH)
	gpio.output(right_lower,gpio.LOW)
	return

def stay():
	global left_upper,left_lower,right_upper,right_lower
	gpio.output(left_upper,gpio.LOW)
	gpio.output(left_lower,gpio.LOW)
	gpio.output(right_upper,gpio.LOW)
	gpio.output(right_lower,gpio.LOW)
	return

def vacuum_on():
	global vacuum_pin
	gpio.output(vacuum_pin,gpio.HIGH)
	print 'Vacuum on'
	return

def vacuum_off():
	global vacuum_pin
	gpio.output(vacuum_pin,gpio.LOW)
	print 'Vacuum off'
	return 
	
def move(data):
	## I couldn't find any switch-case in Python till now.
	## Refer here if needed -- http://stackoverflow.com/a/60236
	if(data=='f'):
		move_forward()
	
	elif(data=='b'):
		move_backward()
	
	elif(data=='r'):
		move_right()
	
	elif(data=='l'):
		move_left()
	
	elif(data=='s'):
		stay()
	
	elif(data=='v'):
		vacuum_on()
	
	elif(data=='o'):
		vacuum_off()
	
	else:
		print 'Not a valid command'
		return

def blinky(pinno,count,delay):
	## this function blinks an LED(if connected) at GPIO pin number pinno, for 'count' number of times, with 'delay' milliseconds between high and low
	if(count==0):
		return
	
	gpio.output(pinno,gpio.HIGH)
	time.sleep(delay)
	gpio.output(pinno,gpio.LOW)
	time.sleep(delay)
	return blinky(pinno,count-1,delay)
	## using recursion here ;) :P 

if __name__ == '__main__':
	
	gpio.setwarnings(False)	
	setup(35,36,37,38,33)
	## 33,35,36,37,38 are just the pin numbers on the Raspberry Pi
	indicator_pin = 40
	gpio.setup(indicator_pin,gpio.OUT)	
	## indicator_pin is just to indicate :P , as an alternative to display in command terminal.
	
	socket = bt.BluetoothSocket(bt.RFCOMM)
        ## We are using RFCOMM protocol here, instead of L2CAP
        ## This is because we need a reliable data transfer. In real world situations, incorrect data transfer is hazardous.
        ## More info here - https://people.csail.mit.edu/albert/bluez-intro/x95.html#protocol-table
	
        accept_details = bind_and_listen(socket)
        
	if( accept_details!=None):
		print 'Connected'

	while True:
		gpio.output(indicator_pin,gpio.HIGH)
		data = receive_data(accept_details)
		gpio.output(indicator_pin,gpio.LOW)
		print data
		if(data=='q'):
			stay()
			print "Are you sure you want to exit ?"
			## We want to as kthe user twice before exiting.
			blinky(indicator_pin,2,0.2)
			if(receive_data(accept_details)=='q'):
				blinky(indicator_pin,6,0.15)
				break
				## If user doesn't quit second time, the loop goes back to initial state, i.e. working state
			else:
				continue
		else:
			move(data)
			## take the data we got above, and pass it to move() function.
			## move()function handles what to do with the data.
			## To understand how move() works, read this about L293D motor driver's working -- 
			## https://www.robotix.in/tutorial/auto/motor_driver/
	gpio.cleanup()	
	## we want the Pi to close all the pins and clean up the mess. Not actually necessary, but good practice.
	## exit()
