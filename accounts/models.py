from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import FileExtensionValidator

# Create your models here.

class RPiUser(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	avatar = models.FileField(null=True, default='default_avatar.png', help_text="upload jpg, jpeg, png files only", validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	mobile_no = models.CharField(max_length=13,default='', unique=True)
	slug = models.SlugField(unique=True, max_length=100)

	def get_absolute_url(self):
		return reverse()

	def __str__(self):
		return self.user.username