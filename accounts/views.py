from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django import forms
from .models import RPiUser
from .forms import UserForm, RPiUserForm
# Create your views here.

def landing_page(request):
	if request.user.is_authenticated:
		return redirect('home')
	return render(request, 'accounts/landing_page.html')

@login_required
def home(request):
	if request.user.is_authenticated:
		return render(request, 'accounts/home.html',{})
	else:
		return redirect('landing-page')

def login_view(request):
	if request.method == 'POST':
	    username = request.POST['username']
	    password = request.POST['password']
	    user = authenticate(request, username=username, password=password)
	    if user is not None:
	        login(request, user)
	        return redirect('home')
	    else:
	    	messages.error(request, "Invalid username or password")
	form = AuthenticationForm()
	return render(request,'accounts/login.html', {'form' : form})

@login_required
def logout_view(request):
	logout(request)
	return render(request, 'accounts/logged_out.html',{})

def register(request):
	if request.method == 'POST':
		user_form = UserForm(request.POST,request.FILES)
		profile_form = RPiUserForm(request.POST,request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password2'])
			new_user.save()
			profile=RPiUser.objects.create(user=new_user)
			profile.mobile_no = profile_form.cleaned_data['mobile_no']
			profile.slug = slugify(new_user.username)
			profile.avatar = profile_form.cleaned_data['avatar']
			profile.save()
			return redirect('accounts:login')
		else:
			messages.error(request, "Mobile number/E-mail already exists")
	else:
		user_form = UserForm()
		profile_form = RPiUserForm()
	return render(request, 'accounts/register.html', {'user_form':user_form, 'profile_form':profile_form})

def voice_recognizer(request):
	if request.method == 'POST':
		if request.is_ajax():
			data = request.POST.get('target')
			print(data)
			if data == 'mobile':
				responseurl = 'mobile:index'
				slug = ''
			elif data == 'tv':
				responseurl = 'television:index'
				slug = ''
			elif data == 'contacts':
				responseurl = 'mobile:all-contacts'
				slug = ''
			elif data == 'create contact':
				responseurl = 'mobile:add-contact'
				slug = ''
			elif data.startswith('call'):
				name = data.split( )
				if len(name) == 1:
					responseurl = 'mobile:call-select-contact'
					slug = ''
				else:
					responseurl = '/mobile/call/'
					slug = name[1]
					print(slug)
					return JsonResponse({
			            'success': True,
						'url': responseurl+slug,
					})
			return JsonResponse({
	            'success': True,
				'url': reverse(responseurl)+slug,
			})
	return redirect('home')