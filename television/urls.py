from django.conf.urls import include, url
from . import views

app_name = 'television'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^brands/$', views.brands, name='brands'),
	url(r'^(?P<slug>[\w-]+)/remote-models/$', views.remote_models,name='remote-models'),
	url(r'^remote/(?P<slug>[\w-]+)/$',views.remote_detail, name='remote-detail'),
	url(r'^remote/(?P<slug>[\w-]+)/add/$', views.add_remote, name='remote-add'),
	url(r'^remote/(?P<slug>[\w-]+)/operate/$', views.remote_area, name='remote-area'),
]
