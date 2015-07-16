# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _

class Restaurant(models.Model):
    # Classe qui représente un restaurant.
    
    restaurateur = models.ForeignKey(User, null=True, blank=True, verbose_name=_("restaurateur"))
    name = models.CharField(max_length=250, verbose_name=_("name"))
    tel = models.CharField(max_length=30, verbose_name=_("telephone"))
    city = models.CharField(max_length=250, verbose_name=_("city"))
    region = models.CharField(max_length=250, verbose_name=_("province/state/region"))
    country = CountryField(verbose_name=_("country"))
    address1 = models.CharField(max_length=250, verbose_name=_("address 1"))
    address2 = models.CharField(max_length=250, null=True, blank=True, verbose_name=_("address 2"))
    zip = models.CharField(max_length=10, verbose_name=_("zip code"))
    image = models.ImageField(upload_to='restaurant/restaurants', blank=True, null=True, verbose_name=_("image"))
        
class Menu(models.Model):
    # Classe qui représente le menu d'un restaurant.
    
    restaurant = models.ForeignKey(Restaurant)
    name = models.CharField(max_length=250, verbose_name=_("name"))
    
class Meal(models.Model):
    # Classe qui représente un plat qui se retrouve sur un menu.
    
    menu = models.ForeignKey(Menu)
    name = models.CharField(max_length=250, verbose_name=_("name"))
    description = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("description"))
    price = models.IntegerField(verbose_name=_("price"))
    