'''Forms for the User management app'''
from __future__ import unicode_literals

from django import  forms
from django.contrib.auth.models import User

class UserForm(forms.Form):
    '''User form with email address, first and last names.

    Creates the user when processed.
    '''
    email = forms.EmailField(label="Email:", max_length=75)
    first_name = forms.CharField(label='First Name:', max_length=40)
    last_name = forms.CharField(label='Last Name:', max_length=40)

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        cleaned_data['email'] = cleaned_data['email'].lower()
        try:
            User.objects.get(email=cleaned_data['email'])
            error_list = self.errors.setdefault('email', self.error_class())
            error_list.append("That email is already in use by another account")
        except User.DoesNotExist:
            pass

        return cleaned_data

class UserEditForm(forms.ModelForm):
    '''Edit user form for name and whether they are active

    Modifies current database entry
    '''
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'is_active']
        help_texts = {'is_active':'Whether the user can login.'}

class PermissionForm(forms.ModelForm):
    '''Edit the groups the user belongs to, and subsequently their permissions

    Modifiers current database entry
    '''
    class Meta:
        model = User
        fields = ['groups']
