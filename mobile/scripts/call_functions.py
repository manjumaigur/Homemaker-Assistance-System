import serial
import RPi.GPIO as GPIO
import os,time

def incoming_call():
	GPIO.setmode(GPIO.BOARD)
	port=serial.Serial("/dev/ttyS0",baudrate=9600,timeout=1)
	data = port.read(10)
	ring=str(data).find("RING")
	if ring>=0:
		port.write("AT+CLIP\r".encode())
		call_details = port.read(30)
		phone_number = str(call_details).split('"')
		phone_number = phone_number[1]
		port.close()
		return phone_number
	else:
		port.close()
		return False

def receive_call():
	GPIO.setmode(GPIO.BOARD)
	port=serial.Serial("/dev/ttyS0",baudrate=9600,timeout=1)
	port.write("ATA\r".encode())
	data = port.read(12)
	received=str(data).find("OK")
	aborted=str(data).find("NO CARRIER")
	if received>=0:
		port.close()
		return True
	if aborted>=0:
		port.close()
		return False
	port.close()
	return False

def abort_call():
	GPIO.setmode(GPIO.BOARD)
	port=serial.Serial("/dev/ttyS0",baudrate=9600,timeout=1)
	port.write("ATH0\r".encode())
	data = port.read(12)
	print(data)
	aborted=str(data).find("OK")
	if aborted>=0:
		port.close()
		return True
	else:
		port.close()
		return False

def check_call_connection():
	GPIO.setmode(GPIO.BOARD)
	port=serial.Serial("/dev/ttyS0",baudrate=9600,timeout=1)
	data = port.read(12)
	disconnected=str(data).find("NO CARRIER")
	if disconnected>=0:
		port.close()
		return True
	else:
		port.close()
		return False