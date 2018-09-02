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

# Create your views here.

def index(request):
	return render(request, 'television/index.html', {})