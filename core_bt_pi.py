### IMPORTANT. DO NOT PROCEED WITHOUT READING ###
### DO NOT TOUCH THE CODE UNLESS AUTHORIZED. IF YOU ARE MAKING ANY CHANGES, COMMENT THE CHANGELOG BELOW
# This code is for the Microprocessors project by Group 41.
# It involves manually controlling the robot through bluetooth.
# PINS 33,34(GND),35,36,37,38,39(GND) ARE RESERVED BY GROUP 41. DO NOT CHANGE THE PINS WITHOUT AUTHORIZATION.

import RPi.GPIO as gpio
import bluetooth as bt
import time

def setup(lu_pinno,ll_pinno,ru_pinno,rl_pinno):
	global left_upper,left_lower,right_upper,right_lower
	left_upper=lu_pinno
	left_lower=ll_pinno
	right_upper=ru_pinno
	right_lower=rl_pinno
	gpio.setmode(gpio.BOARD)
	gpio.setup(left_upper,gpio.OUT)
	gpio.setup(left_lower,gpio.OUT)
	gpio.setup(right_upper,gpio.OUT)
	gpio.setup(right_lower,gpio.OUT)
	# SET ALL PINS TO LOW FIRST
	gpio.output(left_upper,gpio.LOW)
	gpio.output(left_lower,gpio.LOW)
	gpio.output(right_upper,gpio.LOW)
	gpio.output(right_lower,gpio.LOW)
	return

def find_nearby_devices():
	devices = bt.discover_devices()
	i=1
	devices_data = dict()
	if(devices!=None):
		print 'Devices found : '
		for dev in devices:
			device_name = bt.lookup_name(dev)
			devices_data.update({str(i):(device_name,dev)})
			print '[%s] %s %s'%(i,device_name,dev)
			i=i+1
		connect_to_whom=raw_input('Select index of device to connect []')
		return devices_data[connect_to_whom]
	else:
		return None

def bind_and_listen(sock):
#	print bt.get_available_port(bt.RFCOMM)
	port = 1
	sock.bind(("",port))
	print 'The Darth RasPi is now listening to you. Connect to the Dark Lord'
	blinky(indicator_pin,3,0.35)

	sock.listen(1)

	accept_sock,accept_addr = sock.accept()
	return accept_sock

def receive_data(accepted_sock):
	data = accepted_sock.recv(1024)
	return data

def move_forward():
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
	print 'Vacuum on'
	#for now
	return 

	
def move(data):
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
	else:
		return

def blinky(pinno,count,delay):
	if(count==0):
		return
	
	gpio.output(pinno,gpio.HIGH)
	time.sleep(delay)
	gpio.output(pinno,gpio.LOW)
	time.sleep(delay)
	count=count-1
	return blinky(pinno,count,delay)

if __name__ == '__main__':

	setup(35,36,37,38)
	indicator_pin = 33
	gpio.setup(indicator_pin,gpio.OUT)	
	socket = bt.BluetoothSocket(bt.RFCOMM)
        accept_details = bind_and_listen(socket)
	print accept_details

	while True:
		gpio.output(indicator_pin,gpio.HIGH)
		data = receive_data(accept_details)
		gpio.output(indicator_pin,gpio.LOW)
		print data
		if(data=='q'):
			stay()
			print "Are you sure you want to exit ?"
			if(receive_data(accept_details)=='q'):
				blinky(indicator_pin,6,0.15)
				gpio.cleanup()	
				exit()
			else:
				continue
		else:
			move(data)
