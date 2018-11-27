import RPi.GPIO as GPIO
import socket
import time

def irSend(decimalCode):
	HOST='192.168.43.164'
	PORT=4210
	print(decimalCode)
	data=decimalCode+"\r"
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	read=s.connect((HOST,PORT))
	time.sleep(1)
	read=s.sendto(bytes(data,'ascii'),(HOST,PORT))
	time.sleep(2)
	print("sent")
	s.close()