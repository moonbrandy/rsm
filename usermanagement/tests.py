'''Tests for the User Management App'''
from __future__ import unicode_literals, absolute_import

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import mail

from django.contrib.auth.models import User, Permission, Group
from . import views

# pylint: disable=E1103

# Superuser email (and username)
SU_EMAIL = 'superuser@rsm.nz'
# Superuser password
SU_PASSWD = 'password'

def superuser():
    '''Create the super user for the tests'''
    # The superuser
    suser = User.objects.create_superuser(username=SU_EMAIL, password=SU_PASSWD,
                                          email=SU_EMAIL)
    suser.first_name = 'first'
    suser.last_name = 'last'
    suser.save()

def create_user(email, first_name, last_name):
    '''Create a user with email address and, first and last names

    The created User is returned.
    '''
    return User.objects.create_user(username=email, email=email,
                                    first_name=first_name, last_name=last_name,
                                    password=SU_PASSWD)

class CompanyUsersViewTests(TestCase):
    '''Tests of the CompanyUser View'''
    def setUp(self):
        superuser()
        self.client.login(username=SU_EMAIL, password=SU_PASSWD)

    def test_user_list_not_logged_in(self):
        '''Test that when the user is logged out they are redirected away'''
        self.client.logout()
        response = self.client.get(reverse('usermanagement_list'))
        self.assertEqual(302, response.status_code,
                         "The client wasn't redirected to the login page")

    def test_user_list_not_admin(self):
        '''Test the when a non-admin user tries they are redirected away'''
        self.client.logout()
        create_user('normal@example.com', 'normal', 'user')
        self.client.login(username='normal@example.com', password=SU_PASSWD)
        response = self.client.get(reverse('usermanagement_list'))
        self.assertEqual(302, response.status_code,
                         "The client wasn't redirected to the login page")

    def test_user_list_self(self):
        """
        We should only see ourselves in the company user list when no other
        users have been created
        """
        self.client.logout()
        user = create_user('normal@example.com', 'normal', 'user')
        perm_obj = Permission.objects.get_by_natural_key('add_user', 'auth',
                                                         'user')
        user.user_permissions.add(perm_obj)
        self.client.login(username='normal@example.com', password=SU_PASSWD)
        response = self.client.get(reverse('usermanagement_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'normal@example.com')
        self.assertEqual(len(response.context['user_list']), 1)
        self.assertEqual(response.context['user_list'][0].pk,
                         response.context['user'].pk)

    def test_user_list_with_no_users(self):
        """
        We should only see ourselves in the company user list when no other
        users have been created
        """
        response = self.client.get(reverse('usermanagement_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, SU_EMAIL)
        self.assertEqual(len(response.context['user_list']), 1)
        self.assertEqual(response.context['user_list'][0].pk,
                         response.context['user'].pk)

    def test_user_list(self):
        """
        We only want to see users that are in the same company, i.e. the same
        domain
        """
        user1 = create_user('user1@rsm.nz', 'user', 'one')
        user2 = create_user('user2@random.co.nz', 'user', 'two')
        response = self.client.get(reverse('usermanagement_list'))

        self.assertContains(response, user1.email)
        self.assertNotContains(response, user2.email)

class CreateUserViewTests(TestCase):
    '''Tests of the Create User view'''
    def setUp(self):
        superuser()
        self.client.login(username=SU_EMAIL, password=SU_PASSWD)

    def test_auth(self):
        '''Test permissions are applied'''
        url = reverse('usermanagement_add')

        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        user = create_user('tester@rsm.nz', 'user', 'auth')
        self.client.login(username='tester@rsm.nz', password=SU_PASSWD)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        perm_obj = Permission.objects.get_by_natural_key('add_user', 'auth',
                                                         'user')
        user.user_permissions.add(perm_obj)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.client.login(username=SU_EMAIL, password=SU_PASSWD)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_valid_input_form(self):
        """ Testing that we can create multiple new users within our domain """
        mail.outbox = []
        response = self.client.post(reverse('usermanagement_add'),
                                    {'email':'user1@rsm.nz',
                                     'first_name':'user', 'last_name':'one'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(User.objects.all()), 2)
        self.assertEqual(len(mail.outbox), 1)

        response = self.client.post(reverse('usermanagement_add'),
                                    {'email':'user2@rsm.nz',
                                     'first_name':'user', 'last_name':'two'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(User.objects.all()), 3)
        self.assertEqual(len(mail.outbox), 2)

    def test_valid_long_email(self):
        """ Testing that we can create a user with a long email address """
        mail.outbox = []
        response = self.client.post(reverse('usermanagement_add'),
                                    {'email':'thisis.areallyreally.longname@rsm.nz',
                                     'first_name':'user', 'last_name':'one'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(User.objects.all()), 2)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(User.objects.get(id=2).username,
                         'thisis.areallyreally.longname@')

    def test_user_add_normal_admin(self):
        """Non-superuser admin adding a new user
        """
        self.client.logout()
        user = create_user('normal@rsm.nz', 'normal', 'user')
        perm_obj = Permission.objects.get_by_natural_key('add_user', 'auth',
                                                         'user')
        user.user_permissions.add(perm_obj)
        self.client.login(username='normal@rsm.nz', password=SU_PASSWD)
        mail.outbox = []
        self.assertEqual(len(User.objects.all()), 2)
        response = self.client.post(reverse('usermanagement_add'),
                                    {'email':'user1@rsm.nz',
                                     'first_name':'user', 'last_name':'one'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(User.objects.all()), 3)
        self.assertEqual(len(mail.outbox), 1)

        response = self.client.post(reverse('usermanagement_add'),
                                    {'email':'user2@rsm.nz',
                                     'first_name':'user', 'last_name':'two'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(User.objects.all()), 4)
        self.assertEqual(len(mail.outbox), 2)

    def test_invalid_email_domain(self):
        """ Checking that we can't create a user for a domain other than the
        user's domain """
        #super user can add anyone
        response = self.client.post(reverse('usermanagement_add'),
                                    {'email':'user1@random.co.nz',
                                     'first_name':'user', 'last_name':'one'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(User.objects.all()), 2)
        self.assertEqual(len(mail.outbox), 1)

        #normal admin can't
        self.client.logout()
        user = create_user('normal@rsm.nz', 'normal', 'user')
        perm_obj = Permission.objects.get_by_natural_key('add_user', 'auth',
                                                         'user')
        user.user_permissions.add(perm_obj)
        self.client.login(username='normal@rsm.nz', password=SU_PASSWD)
        mail.outbox = []

        response = self.client.post(reverse('usermanagement_add'),
                                    {'email':'user2@random.co.nz',
                                     'first_name':'user', 'last_name':'one'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(User.objects.all()), 3)
        self.assertFormError(response, 'form', 'email',
                             "You don't have permission to create a user for "
                             "that domain")

    def test_duplicate_email_address(self):
        """ Testing that we can't create users with duplicate usernames/email
        address """
        create_user('user1@rsm.nz', 'user', 'last_name')

        response = self.client.post(reverse('usermanagement_add'),
                                    {'email':'user1@rsm.nz',
                                     'first_name':'user', 'last_name':'one'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(User.objects.all()), 2)
        self.assertFormError(response, 'form', 'email',
                             "That email is already in use by another account")

    def test_user_add_not_logged_in(self):
        '''Test that when the user is logged out they are redirected away'''
        self.client.logout()
        response = self.client.get(reverse('usermanagement_add'))
        self.assertEqual(302, response.status_code,
                         "The client wasn't redirected to the login page")

        response = self.client.post(reverse('usermanagement_add'),
                                    {'email':'user1@rsm.nz',
                                     'first_name':'user', 'last_name':'one'})
        self.assertEqual(302, response.status_code,
                         "The client wasn't redirected to the login page")

    def test_user_add_not_admin(self):
        '''Test the when a non-admin user tries they are redirected away'''
        self.client.logout()
        create_user('normal@example.com', 'normal', 'user')
        self.client.login(username='normal@example.com', password=SU_PASSWD)
        response = self.client.get(reverse('usermanagement_add'))
        self.assertEqual(302, response.status_code,
                         "The client wasn't redirected to the login page")

        response = self.client.post(reverse('usermanagement_add'),
                                    {'email':'user1@rsm.nz',
                                     'first_name':'user', 'last_name':'one'})
        self.assertEqual(302, response.status_code,
                         "The client wasn't redirected to the login page")

class UpdateUserViewTests(TestCase):
    '''Tests of the Create User view'''
    def setUp(self):
        superuser()
        create_user('tester@rsm.nz', 'Ali-beth', 'very Unlikely')

    def test_auth(self):
        '''Test permissions are applied'''
        url = reverse('usermanagement_edit', kwargs={'pk': '2'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='tester@rsm.nz', password=SU_PASSWD)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username=SU_EMAIL, password=SU_PASSWD)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_updating_user(self):
        """ Testing that we can update a users within our domain """
        self.client.login(username=SU_EMAIL, password=SU_PASSWD)

        url = reverse('usermanagement_edit', kwargs={'pk': '2'})
        response = self.client.get(url)
        self.assertContains(response, 'Ali-beth')
        self.assertContains(response, 'very Unlikely')

        response = self.client.post(url,
                                    {'first_name':'user', 'last_name':'one', 'is_active': '1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(User.objects.all()), 2)
        user = User.objects.get(id=2)
        self.assertEqual(user.first_name, 'user')
        self.assertEqual(user.last_name, 'one')
        self.assertTrue(user.is_active)


class UserDomainMethodTests(TestCase):  # pylint: disable=R0903
    '''Tests of the user_domain function'''
    def test_input_output(self):
        '''Test the user_domain function's output for various inputs'''
        self.assertEqual(views.user_domain(create_user('u@blah.com.bobbity.boo',
                                                       'blargh', 'darg')),
                         '@blah.com.bobbity.boo')
        self.assertEqual(views.user_domain(create_user('u@blah.com.BOBBITY.boo',
                                                       'blargh', 'darg')),
                         '@blah.com.bobbity.boo')
        self.assertNotEqual(views.user_domain(create_user('u@blah.com.BOBBITY',
                                                          'blargh', 'darg')),
                            '@blah.com.bobbity.boo')
        self.assertEqual(views.user_domain(
            create_user('sdfsdfsdfu@blah.com.BOBBITY.boo', 'blargh', 'darg')),
                         '@blah.com.bobbity.boo')

class SingleUserResetTests(TestCase):
    '''Test the reset of a single user'''

    def setUp(self):
        superuser()
        self.client.login(username=SU_EMAIL, password=SU_PASSWD)
        self.user1 = create_user(SU_EMAIL[5:], 'user', 'harmonic')
        self.user2 = create_user(SU_EMAIL[5:9] + '2' + SU_EMAIL[9:], 'user2',
                                 'harmonic')
        self.user3 = create_user('someone@somewhere.else', 'User', 'somewhere')

    def test_reset_normal_user(self):
        '''Test reseting a normal user's password'''
        response = self.client.get(reverse('usermanagement_reset',
                                           kwargs={'pk': self.user1.id}))
        self.assertContains(response, 'user harmonic will be logged out')
        self.assertContains(response, 'Reset users password')

        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(reverse('usermanagement_reset',
                                            kwargs={'pk': self.user1.id}))
        self.assertEqual(len(mail.outbox), 1)
        self.assertRedirects(response, reverse('usermanagement_list'))

    def test_reset_self(self):
        '''Test reseting our own password'''
        user_pk = User.objects.get(username=SU_EMAIL).id
        response = self.client.get(reverse('usermanagement_reset',
                                           kwargs={'pk': user_pk}))
        self.assertContains(response, '<b>YOU</b> will be logged out')
        self.assertContains(response, 'Reset users password')

        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(reverse('usermanagement_reset',
                                            kwargs={'pk': user_pk}))
        self.assertEqual(len(mail.outbox), 1)
        response = self.client.get(reverse('usermanagement_list'))
        exp_dest = reverse('login') + '?next=' + reverse('usermanagement_list')
        self.assertRedirects(response, exp_dest)

    def test_reset_other_user(self):
        '''Test reseting the password of a user from another org'''
        response = self.client.get(reverse('usermanagement_reset',
                                           kwargs={'pk': self.user3.id}))
        self.assertEqual(response.status_code, 404)

        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(reverse('usermanagement_reset',
                                            kwargs={'pk': self.user3.id}))
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(response.status_code, 404)

class MassUserResetTests(TestCase):
    '''Tests of the mass user reseting functionality'''

    def setUp(self):
        superuser()
        self.client.login(username=SU_EMAIL, password=SU_PASSWD)
        self.user1 = create_user(SU_EMAIL[5:], 'user', 'harmonic')
        self.user2 = create_user(SU_EMAIL[5:9] + '2' + SU_EMAIL[9:], 'user2',
                                 'harmonic')
        self.user3 = create_user('someone@somewhere.else', 'User', 'somewhere')

    def test_multiple_reset(self):
        '''Test reseting multiple users at once'''
        response = self.client.post(reverse('usermanagement_mass_reset'),
                                    {'password_reset':(self.user1.id,
                                                       self.user2.id)})
        self.assertRedirects(response, reverse('usermanagement_list'),
                             msg_prefix='Client should have been redirected to '
                             'the user list')

        response = self.client.logout()

        response = self.client.login(username=self.user1.username,
                                     password=SU_PASSWD)
        self.assertFalse(response,
                         'Login should fail for user with reset password')

        response = self.client.login(username=self.user2.username,
                                     password=SU_PASSWD)
        # Login should fail
        self.assertFalse(response,
                         'Multiple users should have had their password reset')

        self.assertEqual(len(mail.outbox), 2, 'Not enough emails in outbox')


    def test_reset_self(self):
        '''Test mass reset including the active user'''
        data = {'password_reset':(User.objects.get(username=SU_EMAIL).id)}
        self.client.post(reverse('usermanagement_mass_reset'), data)
        response = self.client.get(reverse('usermanagement_list'))
        exp_dest = reverse('login') + '?next=' + reverse('usermanagement_list')
        self.assertRedirects(response, exp_dest,
                             msg_prefix='The user should be logged out and '
                             'asked to login again')

        response = self.client.login(username=SU_EMAIL, password=SU_PASSWD)
        self.assertFalse(response,
                         'Login should fail as the password has changed')

        self.assertEqual(len(mail.outbox), 1, 'Insufficient emails in outbox')

    def test_reset_other_org(self):
        '''Test if we can reset the password of another org'''
        response = self.client.post(reverse('usermanagement_mass_reset'),
                                    {'password_reset':(self.user3.id,)})
        self.assertRedirects(response, reverse('usermanagement_list'),
                             msg_prefix='Client should have been redirected to '
                             'the user list')

        self.assertEqual(len(mail.outbox), 0, 'Too many emails in outbox')

        response = self.client.logout()

        response = self.client.login(username=self.user3.username,
                                     password=SU_PASSWD)
        self.assertTrue(response, 'Login should not fail')


class PermissionTests(TestCase):
    '''Tests of the user permissions functionality'''

    def setUp(self):
        superuser()
        self.user = create_user(SU_EMAIL[5:], 'user', 'harmonic')
        self.grp = Group.objects.create(name='Usermanagement')
        self.grp.permissions.add(Permission.objects.get(codename='add_user'))

    def test_permission(self):
        '''Test if adding a group with a permission provides the permission'''
        # check that user cant access user management area
        self.assertTrue(self.client.login(username=SU_EMAIL[5:],
                                          password=SU_PASSWD))
        response = self.client.get(reverse('usermanagement_list'), follow=True)
        exp_dest = reverse('login') + '?next=' + reverse('usermanagement_list')
        self.assertRedirects(response, exp_dest,
                             msg_prefix='Expected login redirect as user does '
                             'not have permission')

        # check that admin is correctly redirected after changing users
        #permissions
        self.client.login(username=SU_EMAIL, password=SU_PASSWD)
        response = self.client.post(reverse('usermanagement_permission',
                                            args=[self.user.id]),
                                    {'groups':(self.grp.id)}, follow=True)
        self.assertRedirects(response, reverse('usermanagement_list'),
                             msg_prefix='After submitting the form the admin '
                             'should be redirected to the user list')

        # check that user can now access user management area
        self.client.login(username=SU_EMAIL[5:], password=SU_PASSWD)
        response = self.client.get(reverse('usermanagement_list'))
        self.assertEqual(200, response.status_code,
                         'user should have permission to view the user list')
