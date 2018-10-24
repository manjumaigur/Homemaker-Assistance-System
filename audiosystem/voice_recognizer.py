from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from mobile.models import Contact
import os
import requests
import csv

basedir = os.path.abspath(os.path.dirname(__file__))

def preprocess_text_data(raw_text_data):
	if (raw_text_data == 'open home') or (raw_text_data == 'go to home') or (raw_text_data == 'go home') or (raw_text_data == 'open homepage') or (raw_text_data == 'homepage') or (raw_text_data == 'go to homepage') or (raw_text_data == 'go homepage'):
		raw_text_data = "home"
	elif (raw_text_data == 'sign in') or (raw_text_data == 'open login page') or (raw_text_data == 'open sign in page') or (raw_text_data == 'login page') or (raw_text_data == 'log me in') or (raw_text_data == 'sign me in') or (raw_text_data == 'sign in page'):
		raw_text_data = "login"
	elif raw_text_data == 'open mobile':
		raw_text_data = raw_text_data.split( )
		raw_text_data =  raw_text_data[1]
	elif ((raw_text_data == 'open tv') or (raw_text_data == 'open television')):
		raw_text_data = raw_text_data.split( )
		raw_text_data =  raw_text_data[1]
	elif (raw_text_data == 'open contacts') or (raw_text_data == 'show contacts') or (raw_text_data == 'open contact') or (raw_text_data == 'show contact') or (raw_text_data == 'contacts book') or (raw_text_data == 'phone book') or (raw_text_data == 'contact book') or (raw_text_data == 'go to contacts'):
		raw_text_data = "contacts";
	elif (("open" in raw_text_data) or ("show" in raw_text_data)) and (("contacts" in raw_text_data) or ("contact" in raw_text_data)):
		raw_text_data = raw_text_data.split( );
		for text_Data in raw_text_data:
			if (text_Data!="open") and (text_Data!="show") and (text_Data!="contact") and (text_Data!="contacts"):
				raw_text_data =  "open " + "contact " + text_Data
				break
	return raw_text_data

def get_redirect_url(raw_text_data,user):
	data = preprocess_text_data(raw_text_data)
	if data == 'home':
		responseurl = 'home'
		slug = ''
	elif data == 'login':
		responseurl = 'accounts:login'
		slug = ''
	elif data == 'logout':
		responseurl = 'accounts:logout'
		slug = ''
	elif data == 'mobile':
		responseurl = 'mobile:index'
		slug = ''
	elif data == 'tv':
		responseurl = 'television:index'
		slug = ''
	elif data == 'contacts':
		responseurl = 'mobile:all-contacts'
		slug = ''
	elif "open contact" in data:
		name = data.split( )
		try:
			get_contact = Contact.objects.filter(user=user,original_name=name[2])
			if get_contact.count() == 0:
				responseurl = ''
				slug = ''
			elif get_contact.count() == 1:
				responseurl = '/mobile/contact/'
				slug = name[2]+str(user)
			else:
				responseurl = '/mobile/contacts/'
				slug = name[2]
		except:
			pass
		voice_log_data(raw_text_data,responseurl+slug)
		return JsonResponse({
			'success': True,
			'url': responseurl+slug,
		})
	elif data == 'create contact' or data == 'add contact':
		responseurl = 'mobile:add-contact'
		slug = ''
	elif "edit contact" in data:
		name = data.split( )
		responseurl = '/mobile/contact/edit/'
		slug = name[2]+str(user)
		voice_log_data(raw_text_data,responseurl+slug)
		return JsonResponse({
			'success': True,
			'url': responseurl+slug,
		})
	elif "delete contact" in data:
		name = data.split()
		responseurl = '/mobile/contact/delete/'
		slug = name[2]+str(user)
		voice_log_data(raw_text_data,responseurl+slug)
		return JsonResponse({
			'success': True,
			'url': responseurl+slug,
		})
	elif data.startswith('call'):
		name = data.split( )
		if len(name) == 1:
			responseurl = 'mobile:call-select-contact'
			slug = ''
		else:
			responseurl = '/mobile/call/'
			slug = name[1]+str(user)
			voice_log_data(raw_text_data,responseurl+slug)
			return JsonResponse({
				'success': True,
				'url': responseurl+slug,
			})
	elif data.startswith('message'):
		name = data.split( )
		if len(name) == 1:
			responseurl = 'mobile:message-select-contact'
			slug = ''
		else:
			responseurl = '/mobile/message/'
			slug = name[1]+str(user)
			voice_log_data(raw_text_data,responseurl+slug)
			return JsonResponse({
				'success': True,
				'url': responseurl+slug,
			})
	else:
		return 0
	voice_log_data(raw_text_data,str(reverse(responseurl)+slug))
	return JsonResponse({
	    'success': True,
		'url': reverse(responseurl)+slug,
	})

def voice_log_data(raw_text_data,responseurl):
	row = [raw_text_data, responseurl]
	with open(basedir + '/log/voice_log_data.csv', 'a') as csv_fle:
		writer = csv.writer(csv_fle)
		writer.writerow(row)
	csv_fle.close()