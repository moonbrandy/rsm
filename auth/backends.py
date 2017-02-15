'''
Created on 03/02/2017

@author: Danny Wu
'''
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailModelBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL, using email and password.
    """

    def authenticate(self, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
