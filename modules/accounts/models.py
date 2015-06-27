# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class UserDetails(models.Model):
    user = models.OneToOneField(User)
    tel = models.CharField(max_length=30, verbose_name=u"Téléphone")
    city = models.CharField(max_length=250, verbose_name=u"Ville")
    region = models.CharField(max_length=250, verbose_name=u"Province/État/Région")
    country = CountryField(verbose_name=u"Pays")
    address1 = models.CharField(max_length=250, verbose_name=u"Adresse 1")
    address2 = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Adresse 2")
    zip = models.CharField(max_length=10, verbose_name=u"Code postal")
    consent_cp = models.BooleanField(verbose_name=u"J'accepte les conditions d'utilisations")
    
    class Meta:
        app_label = 'accounts'
        db_table = 'accounts_userdetails'
        verbose_name = 'Détails de compte'
        verbose_name_plural = 'Détails de comptes'
        
class UserAddress(models.Model):
    primary = models.BooleanField(verbose_name=u"Adresse primaire")
    city = models.CharField(max_length=250, verbose_name=u"Ville")
    region = models.CharField(max_length=250, verbose_name=u"Province/État/Région")
    country = CountryField(verbose_name=u"Pays")
    address1 = models.CharField(max_length=250, verbose_name=u"Adresse 1")
    address2 = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Adresse 2")
    zip = models.CharField(max_length=10, verbose_name=u"Code postal")
    
    class Meta:
        app_label = 'accounts'
        db_table = 'accounts_useraddress'
        verbose_name = 'Adresse de livraison'
        verbose_name_plural = 'Adresses de livraison'
        