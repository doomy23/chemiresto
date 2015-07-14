# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _

class UserDetails(models.Model):
    user = models.OneToOneField(User, verbose_name=_("user"))
    tel = models.CharField(max_length=30, verbose_name=_("telephone"))
    city = models.CharField(max_length=250, verbose_name=_("city"))
    region = models.CharField(max_length=250, verbose_name=_("province/state/region"))
    country = CountryField(verbose_name=_("country"))
    address1 = models.CharField(max_length=250, verbose_name=_("address 1"))
    address2 = models.CharField(max_length=250, null=True, blank=True, verbose_name=_("address 2"))
    zip = models.CharField(max_length=10, verbose_name=_("zip code"))
    consent_cp = models.BooleanField(verbose_name=_("I agree to the Terms of Use, EULA and Privacy Policy"))
        
class UserAddress(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"))
    default = models.BooleanField(verbose_name=_("default delivery Address"))
    city = models.CharField(max_length=250, verbose_name=_("city"))
    region = models.CharField(max_length=250, verbose_name=_("province/state/region"))
    country = CountryField(verbose_name=_("country"))
    address1 = models.CharField(max_length=250, verbose_name=_("address 1"))
    address2 = models.CharField(max_length=250, null=True, blank=True, verbose_name=_("address 2"))
    zip = models.CharField(max_length=10, verbose_name=_("zip code"))
    