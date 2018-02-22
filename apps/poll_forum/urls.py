from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^forum$', views.forum),
    url(r'^create_poll$', views.create_poll),
    url(r'^newPoll$', views.newPoll),
    url(r'^process/(?P<id>\d+)$', views.process),
]