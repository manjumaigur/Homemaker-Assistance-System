from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import RPiUser

class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name','email', 'password1', 'password2',]

	def clean_email(self):
		if User.objects.filter(email__iexact=self.cleaned_data['email']):
			raise forms.ValidationError("Email id already exists")
		return self.cleaned_data['email']

class RPiUserForm(forms.ModelForm):
	class Meta:
		model = RPiUser
		fields = ['mobile_no', 'avatar',]

	def clean_mobile_no(self):
		if RPiUser.objects.filter(mobile_no__iexact=self.cleaned_data['mobile_no']):
			raise forms.ValidationError("Mobile number already exists")
		return self.cleaned_data['mobile_no']