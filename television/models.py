from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import datetime

# Create your models here.

class Brand(models.Model):
	name = models.CharField(max_length=100, default='')
	slug = models.SlugField(unique=True, max_length=500)	#slug=name

	def __str__(self):
		return self.name

class Remote(models.Model):
	user = models.ManyToManyField(settings.AUTH_USER_MODEL)
	brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
	model = models.CharField(max_length=100, default='')
	description = models.TextField(default='')
	REMOTE_TYPES = (
		('t', 'television'),
		('s', 'setup-box'),
	)
	remote_type = models.CharField(max_length=1, default='s', choices=REMOTE_TYPES, blank=False, null=True)
	remotes_in_use = models.IntegerField(default=0)
	ir_code_file = models.FileField(null=True, help_text="upload .json files only", validators=[FileExtensionValidator(['json'])])
	slug = models.SlugField(unique=True, max_length=500)  #slug=brand-model

	def __str__(self):
		return str(self.brand) + "-" + self.model