from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('(?P<path>.*)', views.receive_url, name='receive_url'),
    ]
