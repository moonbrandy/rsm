'''
Created on 8/09/2014

@author: lee
'''
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.contrib.auth import views

from . import forms

urlpatterns = [
    url(r'^login/$', views.login,
        kwargs={'authentication_form': forms.RSMAuthenticationForm},
        name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^password_change/$', views.password_change, name='password_change'),
    url(r'^password_change/done/$', views.password_change_done,
        name='password_change_done'),
    url(r'^password_reset/$', views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done,
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete,
        name='password_reset_complete'),
]
