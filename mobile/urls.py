from django.conf.urls import include, url
from . import views

app_name = 'mobile'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^contacts/$', views.contact_list, name='all-contacts'),
	url(r'^contacts/(?P<slug>[\w-]+)/$', views.custom_contact_list, name='custom-contacts'),
	url(r'^contact/add/$', views.add_contact, name='add-contact'),
	url(r'^contact/edit/(?P<slug>[\w-]+)/$', views.edit_contact, name='edit-contact'),
	url(r'^contact/delete/(?P<slug>[\w-]+)/$', views.DeleteContact.as_view(), name='delete-contact'),
	url(r'^contact/(?P<slug>[\w-]+)/$', views.contact_detail, name="contact"),
	url(r'^call/select-contact/$', views.call_select_contact, name="call-select-contact"),
	url(r'^call/(?P<slug>[\w-]+)/$', views.call, name="call"),
	url(r'^check_incoming_call/$', views.incoming_call_check, name='check-incoming-call'),
	url(r'^message/select-contact/$', views.message_select_contact, name="message-select-contact"),
	url(r'^message/(?P<slug>[\w-]+)/$', views.chatroom, name="message"),
]