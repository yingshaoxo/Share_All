from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^(?P<user_name>[A-Za-z0-9]+)/$', views.detail, name='detail'),
]

