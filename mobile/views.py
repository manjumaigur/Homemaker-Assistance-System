from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils.text import slugify
from django.utils import timezone
from django.db.models import Q
from .models import Contact, Message
from accounts.models import RPiUser
from .forms import ContactForm, MessageForm
from .scripts import call_sms_functions

# Create your views here.

@login_required
def index(request):
	profile = get_object_or_404(RPiUser, user=request.user)
	return render(request, 'mobile/index.html', {'profile':profile})

@login_required
def contact_list(request):
	contacts = Contact.objects.filter(user=request.user)
	return render(request, 'mobile/contacts.html', {'contacts':contacts})

@login_required
def custom_contact_list(request,slug):
	contacts = Contact.objects.filter(user=request.user,original_name=slug)
	return render(request, 'mobile/contacts.html', {'contacts':contacts})

@login_required
def contact_detail(request,slug):
	contact = get_object_or_404(Contact, slug=slug)
	return render(request, 'mobile/contact_detail.html', {'contact':contact})

@login_required
def add_contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST, request.FILES)
		if form.is_valid():
			new_form = form.save(commit=False)
			new_contact = Contact.objects.create(user = request.user)
			new_contact.original_name = form.cleaned_data['name'].lower()
			try:
				contact_name = Contact.objects.filter(user=request.user, original_name=new_contact.original_name)
				print(contact_name)
				no_contacts = contact_name.count()
				print(no_contacts)
				if no_contacts>0:
					new_contact.name = new_contact.original_name + str(no_contacts)
				else:
					new_contact.name = new_contact.original_name	
			except Contact.DoesNotExist:
				new_contact.name = new_contact.original_name
			new_contact.slug = slugify(new_contact.name+str(request.user))
			new_contact.phone_number = form.cleaned_data['phone_number']
			new_contact.avatar = form.cleaned_data['avatar']
			new_contact.save()
			return redirect('mobile:contact', slug=new_contact.slug)
	else:
		form = ContactForm()
	return render(request, 'mobile/add_contact.html', {'form':form})

@login_required
def edit_contact(request, slug):
	contact = get_object_or_404(Contact, slug=slug)
	if request.method == 'POST':
		form = ContactForm(request.POST, request.FILES, instance=contact)
		if form.is_valid():
			new_form = form.save(commit=False)
			if contact.original_name != form.cleaned_data['name'].lower():
				contact.original_name = form.cleaned_data['name'].lower()
				try:
					contact_name = Contact.objects.filter(user=request.user, original_name=contact.original_name)
					print(contact_name)
					no_contacts = contact_name.count()
					print(no_contacts)
					if no_contacts>0:
						contact.name = contact.original_name + str(no_contacts)
					else:
						contact.name = contact.original_name
				except Contact.DoesNotExist:
					contact.name = contact.original_name
				contact.slug = slugify(contact.name+str(request.user))
			form.save()
			contact.save()
			return redirect('mobile:contact', slug=contact.slug)
		else:
			messages.error(request, "Error processing form. Please fill the correct details")
	else:
		form = ContactForm(instance=contact)
	return render(request, 'mobile/edit_contact.html', {'form':form,'contact':contact})

@method_decorator(login_required, name='dispatch')
class DeleteContact(DeleteView):
    model = Contact
    template_name = 'mobile/contact_confirm_delete.html'
    success_url = reverse_lazy('mobile:all-contacts')

@login_required
def call_select_contact(request):
	contacts = Contact.objects.filter(user=request.user)
	return render(request, 'mobile/call_select_contact.html', {'contacts':contacts})

@login_required
def call(request, slug):
	contact = get_object_or_404(Contact, slug=slug)
	return render(request, 'mobile/call.html', {'contact':contact})

@login_required
def message_select_contact(request):
	contacts = Contact.objects.filter(user=request.user)
	return render(request, 'mobile/message_select_contact.html', {'contacts':contacts})

@login_required
def chatroom(request,slug):
	contact = get_object_or_404(Contact, slug=slug)
	messages = Message.objects.filter(Q(user=request.user) & (Q(to_contact=contact) | Q(from_contact=contact)))
	if request.method == 'POST':
		form = MessageForm(request.POST)
		if form.is_valid():
			new_form = form.save(commit=False)
			return redirect('home')
	else:		
		form = MessageForm()
	return render(request, 'mobile/chatroom.html', {'contact':contact, 'messages':messages, 'form':form})

@login_required
def message(request,slug):
	contact = get_object_or_404(Contact, slug=slug)

@login_required
def incoming_call_sms_check(request):
	call_sms_coming = call_sms_functions.incoming_call_sms(request.user)
	if call_sms_coming:
		call_sms_coming = call_sms_coming.split(";")
		message_coming = False
		call_coming = False
		contact_in_phonebook = False
		contact_name = ''
		contact_photo = ''
		contact_number = ''
		if call_sms_coming[0]=="CALL":
			contact_number = call_sms_coming[1]
			incoming_number = contact_number[3:]
			try:
				contact_details = Contact.objects.get(user=request.user, phone_number=incoming_number)
				call_coming = True
				message_coming = False
				contact_in_phonebook = True
				contact_name = contact_details.name
				contact_number = contact_details.phone_number
				contact_photo = contact_details.avatar.url
			except Contact.DoesNotExist:
				call_coming = True
				message_coming = False
		elif call_sms_coming[0]=="MESSAGE":
			message_coming = True
			call_coming = False
			new_message_id = call_sms_coming[1]
			new_message = get_object_or_404(Message,id=new_message_id)
			contact_in_phonebook = not new_message.unknown_contact
			if contact_in_phonebook:
				contact_number = new_message.from_contact.phone_number
				contact_name = new_message.from_contact.name
				contact_photo = new_message.from_contact.avatar.url
				contact_details = Contact.objects.get(user=request.user, phone_number=contact_number)
		return JsonResponse({
			'call_coming': call_coming,
			'message_coming':message_coming,
			'contact_in_phonebook': contact_in_phonebook,
			'contact_name': contact_name,
			'contact_number': contact_number,
			'contact_photo': contact_photo,
			'smsSlug': contact_details.slug,
		})

@login_required
def receive_call(request):
	flag = call_sms_functions.receive_call()
	return JsonResponse({
		'success':flag
	})

@login_required
def abort_call(request):
	flag = call_sms_functions.abort_call()
	return JsonResponse({
		'success':flag
	})

@login_required
def check_call_connection(request):
	flag = call_sms_functions.check_call_connection()
	connected = False
	if flag:
		connected = False
	else:
		connected = True
	return JsonResponse({
		'connected':connected
	})