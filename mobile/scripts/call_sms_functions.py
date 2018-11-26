import serial
import RPi.GPIO as GPIO
import os,time
from django.contrib.auth.models import User
from accounts.models import RPiUser
from mobile.models import Message

def incoming_call_sms(module_user):
	GPIO.setmode(GPIO.BOARD)
	port=serial.Serial("/dev/ttyS0",baudrate=9600,timeout=1)
	data = port.read(10)
	ring=str(data).find("RING")
	new_message = str(data).find("+CMTI")
	if ring>=0:
		port.write("AT+CLIP\r".encode())
		call_details = port.read(30)
		phone_number = str(call_details).split('"')
		phone_number = phone_number[1]
		port.close()
		return "CALL"+";"+phone_number
	elif new_message>=0:
		flag=save_message(module_user)
		flag=flag.split(";")
		if flag[1]:
			msg_id=flag[0]
		else:
			pass
		return "MESSAGE"+";"+msg_id
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

def send_sms(module_user,mobile_number,text):
	GPIO.setmode(GPIO.BOARD)
	port=serial.Serial("/dev/ttyS0",baudrate=9600,timeout=1)
	port.write("AT+CMGF=1".encode())
	print("1")
	time.sleep(1)
	port.write(('AT+CMGS="'+mobile_number+'"\r').encode())
	print("2")
	time.sleep(2)
	port.write(text.encode())
	print("3")
	time.sleep(1)
	port.write('\x1A'.encode())
	time.sleep(1)
	print('sending.....')
	while True:
		data = port.read(40)
		flag = str(data).find("+CMGS:")
		print(data)
		if flag>=0:
			module_user = User.objects.get(username=module_user)
			local_user = RPiUser.objects.get(user=module_user)
			from_contact = Contact.objects.get(user=module_user, phone_number=local_user.mobile_no)
			to_contact = Contact.objects.get(user=module_user,phone_number=mobile_number)
			new_message = Message.objects.create(user=module_user,from_contact=from_contact,to_contact=to_contact)
			new_message.text = text
			new_message.unknown_contact = False
			new_message.save()
			time.sleep(1)
			port.close()
			return True
	print("closed")
	port.close()
	return False

def save_message(module_user):
	GPIO.setmode(GPIO.BOARD)
	port=serial.Serial("/dev/ttyS0",baudrate=9600,timeout=1)
	port.write('AT+CMGL="REC UNREAD"\r'.encode())
	data=port.read(1000)
	time.sleep(1)
	sms_no=str(data).split("CMGL")
	port.write(('AT+CMGR='+(len(sms_no)-1)+"\r").encode())
	data=port.read(1000)
	flag=str(data).find("OK")
	if flag>=0:
		msg=str(data).split("\\r\\n")
		msg_content=msg[2]
		msg_details=(msg[1].split(","))[1]
		module_user = User.objects.get(username=module_user)
		store_msg = Message.objects.create(user=module_user)
		local_user = RPiUser.objects.get(user=module_user)
		store_msg.to_contact = Contact.objects.get(user=module_user, phone_number=local_user.mobile_no)
		store_msg.text = msg_content
		store_msg.is_incoming = True
		store_msg.is_outgoing = False
		store_msg.received_datetime = (msg[1].split(","))[3]
		from_contact = msg_details[1:len(msg_details)-1]
		from_contact = from_contact[3:]
		contact_in_phonebook = False
		contact_name = ''
		try:
			contact_details = Contact.objects.get(user=module_user, phone_number=from_contact)
			contact_in_phonebook = True
		except Contact.DoesNotExist:
			contact_in_phonebook = False
		if contact_in_phonebook:
			contact_name = contact_details.name
			store_msg.unknown_contact = False
			store_msg.from_contact = contact_details
			store_msg.save()
			port.close()
			return store_msg.id+";"+"1"		#id;saved
		else:
			store_msg.unknown_contact = True
			store_msg.unknown_mobile = from_contact
			store_msg.save()
			port.close()
			return store_msg.id+";"+"1"		#id;saved
	else:
		port.close()
		return "0"+";"+"0"