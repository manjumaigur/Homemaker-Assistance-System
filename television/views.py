from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse 
from django.template import Template, Context, loader
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Q
from .models import Brand, Remote

# Create your views here.

def index(request):
	remotes =Remote.objects.filter(user=request.user)
	return render(request, 'television/index.html', {'remotes':remotes})

def brands(request):
	brands = Brand.objects.all()
	return render(request, 'television/brands.html', {'brands':brands})

def remote_models(request,slug):
	brand = get_object_or_404(Brand, slug=slug)
	models = Remote.objects.filter(brand=brand)
	return render(request, 'television/remote_models.html', {'models':models,'brand':brand})

def remote_detail(request,slug):
	remote = get_object_or_404(Remote, slug=slug)
	try:
		flag_remote = Remote.objects.get(user=request.user,slug=slug)
		if flag_remote:
			flag = 1
	except:
		flag = 0
	return render(request, 'television/remote_detail.html', {'remote':remote,'flag':flag})

def add_remote(request, slug):
	remote = get_object_or_404(Remote, slug=slug)
	try:
		flag_remote = Remote.objects.get(user=request.user,slug=slug)
		if flag_remote:
			messages.info(request, "Remote already in your account")
	except Remote.DoesNotExist:
		remote.user.add(request.user)
		remote.remotes_in_use +=1
		remote.save()
		messages.success(request, "Remote added successfully to your account")
	return redirect('television:index')

def remote_area(request, slug):
	remote = get_object_or_404(Remote, slug=slug)
	try:
		flag_remote = Remote.objects.get(user=request.user,slug=slug)
		if flag_remote:
			return render(request, 'television/remote_area.html', {'remote':remote})
	except:
		messages.error(request, 'No such remote exists in your account')
		return redirect('television:index')
		
