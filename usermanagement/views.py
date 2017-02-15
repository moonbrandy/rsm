'''Views for the User Management app'''
from __future__ import unicode_literals, absolute_import

from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.generic import ListView, FormView, DetailView, UpdateView
from django.core.urlresolvers import reverse
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib import messages

from .forms import UserForm, UserEditForm, PermissionForm

# pylint: disable=R0901

def can_manage_users(user):
    '''Checks if a user can manage users'''
    return user.is_staff or user.has_perm('auth.add_user')

class CompanyUsersView(ListView):
    '''View of the list of the users that the current logged in user can view'''
    template_name = 'usermanagement/user_list.html'
    # Model = User

    def get_queryset(self):
        '''Get the queryset.'''
        return User.objects.all()

class NewUserView(FormView):
    '''View to add new users

    Must have email address from the same domain.

    Welcome emails uses usermanagement/welcome_email.txt for the body and
    usermanagement/welcome_email_subject.txt for the subject line.
    '''
    template_name = 'usermanagement/new_user.html'
    form_class = UserForm

    def form_valid(self, form):
        '''Form is valid, process

        If the email doesn't match, the form is invalid and forward
        responsibility there.
        '''
        if (self.request.user.is_superuser):
            user = self.process_add_user(form)
            messages.success(self.request, 'New user added. Email sent to %s'
                             ' to invite them to login.' % user.email)
            return HttpResponseRedirect(reverse('usermanagement_list'))
        else:
            error_list = form.errors.setdefault('email', form.error_class())
            error_list.append("You don't have permission to create a user for "
                              "that domain")
            del form.cleaned_data['email']

        return self.form_invalid(form)

    def process_add_user(self, form):
        '''Process the form, save the user and email reset password'''

        cleand = form.cleaned_data
        user = User.objects.create_user(email=cleand.get('email'),
                                        username=cleand.get('email')[:30])
        user.first_name = cleand.get('first_name')
        user.last_name = cleand.get('last_name')
        temp_password = User.objects.make_random_password()
        user.set_password(temp_password)
        user.save()

        current_site = get_current_site(self.request)
        context = {'token': default_token_generator.make_token(user),
                   'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                   'user': user,
                   'email': user.email,
                   'protocol': 'https' if self.request.is_secure() else 'http',
                   'domain': current_site.domain,
                   'site_name': current_site.name}
        body = render_to_string('usermanagement/welcome_email.txt',
                                context)
        subject = render_to_string('usermanagement/welcome_email_subject.txt',
                                   context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        user.email_user(subject=subject, message=body)

        return user

class UpdateUser(UpdateView):
    '''Update the details for one user'''
    template_name = 'usermanagement/edit_user.html'
    form_class = UserEditForm
    model = User
    context_object_name = 'ruser'

    def get_queryset(self):
        '''Get the queryset.'''
        return User.objects.all()

    def get_success_url(self):
        return reverse('usermanagement_list')

class ResetUser(DetailView):
    '''View of the list of the users that the current logged in user can view'''
    template_name = 'usermanagement/reset_user.html'
    model = User
    context_object_name = 'ruser'

    def get_queryset(self):
        '''Get the queryset. Users with the same email domain'''
        return User.objects.all()

    def post(self, request, *args, **kwargs): #pylint: disable=W0613
        '''Accept a post request, reset the user's password'''
        user = self.get_object()
        reset_user(self, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self): #pylint: disable=R0201
        '''Get the url to redirect to on success'''
        return reverse('usermanagement_list')

class MassReset(ListView):
    '''View of the list of the users that the current logged in user can view'''
    template_name = 'usermanagement/mass_password_reset.html'

    def post(self, request, *args, **kwargs): #pylint: disable=W0613
        '''Accept a post request, reset the user's password'''
        for user_pk in request.POST.getlist('password_reset'):
            user = User.objects.get(pk=user_pk)
            reset_user(self, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self): #pylint: disable=R0201
        '''Get the url to redirect to on success'''
        return reverse('usermanagement_list')

    def get_queryset(self):
        '''Get the queryset'''
        users = User.objects.all()
        # we dont want to view the current user
        users = users.exclude(id=self.request.user.id).all()
        return users

class UpdatePermission(UpdateView):
    '''Update groups and permissions for a user'''
    template_name = 'usermanagement/user_permission.html'
    form_class = PermissionForm
    context_object_name = 'ruser'

    def get_queryset(self):
        '''Get the queryset.'''
        return User.objects.all()

    def get_success_url(self):
        '''Get the url to redirect to on success'''
        return reverse('usermanagement_list')


def reset_user(view, user=None):
    '''Reset the user's or view object's password'''
    if user is None:
        user = view.get_object()

    temp_password = User.objects.make_random_password()
    user.set_password(temp_password)
    user.save()

    current_site = get_current_site(view.request)
    context = {'token': default_token_generator.make_token(user),
               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
               'user': user,
               'email': user.email,
               'protocol': 'https' if view.request.is_secure() else 'http',
               'domain': current_site.domain,
               'site_name': current_site.name}
    body = render_to_string('usermanagement/reset_email.txt',
                            context)
    subject = render_to_string('usermanagement/reset_email_subject.txt',
                               context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    user.email_user(subject=subject, message=body)
