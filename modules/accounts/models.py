# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class UserDetails(models.Model):
    user = models.OneToOneField(User)
    tel = models.CharField(max_length=30, verbose_name=u"Téléphone")
    city = models.CharField(max_length=250, verbose_name=u"Ville")
    country = CountryField(verbose_name=u"Pays")
    address1 = models.CharField(max_length=250, verbose_name=u"Adresse 1")
    address2 = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Adresse 2")
    zip = models.CharField(max_length=10, verbose_name=u"Code postal")
    consent_cp = models.BooleanField(verbose_name=u"J'accepte les conditions d'utilisations")
    