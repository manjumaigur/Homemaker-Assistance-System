from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import datetime

# Create your models here.

class Contact(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	name = models.CharField(max_length=50, default='')
	avatar = models.FileField(null=True, default='default_avatar.png', help_text="upload jpg, jpeg, png files only", validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	phone_number = models.CharField(max_length=13, default='', unique=True)
	slug = models.SlugField(unique=True, max_length=500)

	def get_absolute_url(self):
		return reverse('mobile:contact-detail')

	def __str__(self):
		return self.name + " " + self.phone_number

class Message(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	to_contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='%(class)s_to_contact')
	from_contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='%(class)s_from_contact',blank=True,null=True)
	text = models.CharField(max_length=2000,blank=True,null=True)
	sent_datetime = models.DateTimeField(default=timezone.now)	#status - sending
	delivered_datetime = models.DateTimeField(default=timezone.now)	#status - delivered
	received_datetime = models.DateTimeField(default=timezone.now)
	is_incoming = models.BooleanField(default=False)
	is_outgoing = models.BooleanField(default=True)
	is_replied = models.BooleanField(default=False)
	unknown_contact = models.BooleanField(default=True)
	STATUS_CHOICES = (
		('s', 'sending'),
		('d', 'delivered'),		#equivalent to sent and if delivered then status is successful
		('r', 'received'),
		('f', 'fail'),
	)
	status = models.CharField(max_length=1, default='s', choices=STATUS_CHOICES, blank=False, null=True)

	def __str__(self):
		return str(self.to_contact)

class Call(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	to_contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='%(class)s_to_contact')
	from_contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='%(class)s_from_contact',blank=True,null=True)
	called_datetime = models.DateTimeField(default=timezone.now)
	received_datetime = models.DateTimeField(default=timezone.now)
	aborted_datetime = models.DateTimeField(default=timezone.now)
	duration = models.CharField(max_length=15,blank=True,null=True)
	is_outgoing = models.BooleanField(default=True)
	is_incoming = models.BooleanField(default=False)
	is_missed_call = models.BooleanField(default=True)
	is_received = models.BooleanField(default=False)
	unknown_contact = models.BooleanField(default=True)
	STATUS_CHOICES = (
		('c', 'calling'),
		('r', 'received'),
		('o', 'ongoing'),
		('h', 'hold'),
		('a', 'aborted'),
		('s', 'success'),
		('f', 'fail'),
	)
	status = models.CharField(max_length=1, default='c', choices=STATUS_CHOICES, blank=False, null=True)

	def __str__(self):
		return str(self.to_contact) + str(self.from_contact)