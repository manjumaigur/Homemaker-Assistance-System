from django import forms
from django.core.exceptions import ValidationError
from django.core import validators
from .models import Contact, Message

class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = ['name', 'phone_number', 'avatar']

class MessageForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = ['text',]
		widgets = {'text':forms.TextInput(attrs={'class':'form-control','rows':5,})}