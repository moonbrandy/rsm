'''
Created on 03/02/2017

@author: Danny Wu
'''
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

class RSMAuthenticationForm(AuthenticationForm):
    '''Authentication form for the Analytics hub

    Username in form is actually the email address'''

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(email=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return self.cleaned_data
