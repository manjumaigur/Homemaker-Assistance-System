from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Q
from .models import Contact
from .forms import ContactForm, MessageForm

# Create your views here.

@login_required
def index(request):
	return render(request, 'mobile/index.html', {})

@login_required
def contact_list(request):
	contacts = Contact.objects.filter(user=request.user)
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
			new_contact.name = form.cleaned_data['name']
			new_contact.slug = slugify(new_contact.name)
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
			if contact.name != form.cleaned_data['name']:
				contact.slug = slugify(form.cleaned_data['name'])
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
def message(request,slug):
	contact = get_object_or_404(Contact, slug=slug)
	form = MessageForm()
	return render(request, 'mobile/message.html', {'contact':contact,'form':form})

