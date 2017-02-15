'''Models for the spectrum db application
'''

from __future__ import unicode_literals, absolute_import

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from djstripe.models import Customer


class RSMUserProfile(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    credit = models.FloatField(default=0.0)
    are_id = models.IntegerField(null=True,blank=True)
    are_account = models.CharField(max_length=100,null=True,blank=True)
    are_password = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return "Customer: %s has %s" % (str(self.customer), str(self.credit))

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(subscriber=instance)

@receiver(post_save, sender=Customer)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        RSMUserProfile.objects.create(customer=instance)