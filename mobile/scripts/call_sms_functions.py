import serial
import RPi.GPIO as GPIO
import os,time
from django.contrib.auth.models import User
from accounts.models import RPiUser
from mobile.models import Message,Contact

GPIO.setmode(GPIO.BOARD)
port=serial.Serial("/dev/ttyS0",baudrate=9600,timeout=1)

def connect_to_port():
	try:
		port=serial.Serial("/dev/ttyS0",baudrate=9600,timeout=1)
	except serial.serialutil.SerialException:
		port.close()
		time.sleep(1)
		port.open()

def incoming_call_sms(module_user):
	connect_to_port()
	data = port.read(10)
	ring=str(data).find("RING")
	new_message = str(data).find("+CMTI")
	if ring>=0:
		port.write("AT+CLIP\r".encode())
		call_details = port.read(30)
		phone_number = str(call_details).split('"')
		phone_number = phone_number[1]
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
		return False

def receive_call():
	connect_to_port()
	port.write("ATA\r".encode())
	data = port.read(12)
	received=str(data).find("OK")
	aborted=str(data).find("NO CARRIER")
	if received>=0:
		return True
	if aborted>=0:
		return False
	return False

def make_call(phone_number):
	connect_to_port()
	port.write(("ATD"+phone_number+";\r").encode())
	time.sleep(2)
	data = port.read(10)
	connected = str(data).find("OK")
	disconnected = str(data).find("NO CARRIER")
	if connected>=0:
		return True
	else:
		return False

def abort_call():
	connect_to_port()
	port.write("ATH0\r".encode())
	data = port.read(12)
	print(data)
	aborted=str(data).find("OK")
	if aborted>=0:
		return True
	else:
		return False

def check_call_connection():
	connect_to_port()
	data = port.read(12)
	disconnected=str(data).find("NO CARRIER")
	if disconnected>=0:
		return True
	else:
		return False

def send_sms(module_user,mobile_number,text):
	connect_to_port()
	sms='AT+CMGS="'+mobile_number+'"\r'
	port.write(sms.encode())
	time.sleep(2)
	data=port.read(60)
	port.write(text.encode())
	time.sleep(1)
	port.write('\x1A'.encode())
	while True:
		data = port.read(40)
		flag = str(data).find("+CMGS:")
		print(data)
		if flag>=0:
			module_user = User.objects.get(username=module_user)
			local_user = RPiUser.objects.get(user=module_user)
			from_contact = Contact.objects.get(user=module_user, slug=str(module_user)+'RPiDefaultUser')
			to_contact = Contact.objects.get(user=module_user,phone_number=mobile_number)
			new_message = Message.objects.create(user=module_user,from_contact=from_contact,to_contact=to_contact)
			new_message.text = text
			new_message.unknown_contact = False
			new_message.save()
			time.sleep(1)
			return True
	print("closed")
	return False

def save_message(module_user):
	connect_to_port()
	port.write('AT+CMGL="ALL"\r'.encode())
	data=port.read(1000)
	time.sleep(1)
	sms_no=str(data).split("CMGL")
	port.write(('AT+CMGR=1\r').encode())
	data=port.read(1000)
	flag=str(data).find("OK")
	if flag>=0:
		msg=str(data).split("\\r\\n")
		msg_content=msg[2]
		msg_details=(msg[1].split(","))[1]
		module_user = User.objects.get(username=module_user)
		local_user = RPiUser.objects.get(user=module_user)
		to_contact = Contact.objects.get(user=module_user,slug=str(module_user)+'RPiDefaultUser')
		store_msg = Message.objects.create(user=module_user,to_contact=to_contact)
		store_msg.text = msg_content
		store_msg.is_incoming = True
		store_msg.is_outgoing = False
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
			delete_all_sms()
			return str(store_msg.id)+";"+"1"		#id;saved
		else:
			unknown_contact = Contact.objects.create(user=module_user,phone_number=from_contact,name=from_contact,original_name=from_contact,slug=from_contact+str(module_user))
			unknown_contact.unknown = True
			store_msg.from_contact = unknown_contact
			store_msg.unknown_contact = True
			store_msg.unknown_mobile = from_contact
			store_msg.save()
			unknown_contact.save()
			delete_all_sms()
			return str(store_msg.id)+";"+"1"		#id;saved
	else:
		delete_all_sms()
		return "0"+";"+"0"

def delete_all_sms():
	connect_to_port()
	port.write("AT+CMGD=1,4\r".encode())
	time.sleep(1)
	data=port.read(50)
	flag = str(data).find("OK")
	if flag>=0:
		return True
	else:
		return False