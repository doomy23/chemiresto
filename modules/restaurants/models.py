# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _

class Restaurant(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=_("restaurateur"))
    name = models.CharField(max_length=250, verbose_name=_("name"))
    tel = models.CharField(max_length=30, verbose_name=_("telephone"))
    city = models.CharField(max_length=250, verbose_name=_("city"))
    region = models.CharField(max_length=250, verbose_name=_("province/state/region"))
    country = CountryField(verbose_name=_("country"))
    address1 = models.CharField(max_length=250, verbose_name=_("address 1"))
    address2 = models.CharField(max_length=250, null=True, blank=True, verbose_name=_("address 2"))
    zip = models.CharField(max_length=10, verbose_name=_("zip code"))
    
    image = models.ImageField(upload_to='restaurants', verbose_name=_("image"), blank=True, null=True)
    
    admin_order_field = 'name'
    
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        app_label = 'restaurants'
        db_table = 'restaurants_restaurant'
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'
        
class Meal(models.Model):
    restaurant = models.ForeignKey(Restaurant, verbose_name=_("restaurant"))
    name = models.CharField(max_length=250, verbose_name=_("name"))
    image = models.ImageField(upload_to='restaurants/meals', verbose_name=_("image"), blank=True, null=True)
    
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        app_label = 'restaurants'
        db_table = 'restaurants_meal'
        verbose_name = 'Repas'
        verbose_name_plural = 'Repas'

class MealTag(models.Model):
    tag = models.CharField(max_length=250, verbose_name=_("tag"))
    meals = models.ManyToManyField(Meal, verbose_name=_("meals"))
    
    class Meta:
        app_label = 'restaurants'
        db_table = 'restaurants_mealtag'
        verbose_name = 'Tag de repas'
        verbose_name_plural = 'Tag de repas'
    