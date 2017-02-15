'''Url Config for the User Management app'''
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url
from django.contrib.auth.decorators import user_passes_test

from . import views

access_test = user_passes_test(views.can_manage_users) #pylint: disable=C0103

urlpatterns = [
    url(r'^$', access_test(views.CompanyUsersView.as_view()),
        name='usermanagement_list'),
    url(r'^add/$', access_test(views.NewUserView.as_view()),
        name='usermanagement_add'),
    url(r'^update/(?P<pk>[0-9]+)/$', access_test(views.UpdateUser.as_view()),
        name='usermanagement_edit'),
    url(r'^reset/(?P<pk>[0-9]+)/$', access_test(views.ResetUser.as_view()),
        name='usermanagement_reset'),
    url(r'^reset/$', access_test(views.MassReset.as_view()),
        name='usermanagement_mass_reset'),
    url(r'^permission/(?P<pk>[0-9]+)/$',
        access_test(views.UpdatePermission.as_view()),
        name='usermanagement_permission'),
]
