from django.conf.urls import url
from . import views

app_name = 'audiosystem'

urlpatterns = [
	url(r'^voice-recognizer/$', views.voice_recognizer, name="voice-recognizer"),
]