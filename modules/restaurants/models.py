# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class Restaurant(models.Model):
    user = models.ForeignKey(User, verbose_name=u"Propriétaire")
    name = models.CharField(max_length=250, verbose_name="Nom")
    tel = models.CharField(max_length=30, verbose_name=u"Téléphone")
    city = models.CharField(max_length=250, verbose_name=u"Ville")
    region = models.CharField(max_length=250, verbose_name=u"Province/État/Région")
    country = CountryField(verbose_name=u"Pays")
    address1 = models.CharField(max_length=250, verbose_name=u"Adresse 1")
    address2 = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Adresse 2")
    zip = models.CharField(max_length=10, verbose_name=u"Code postal")
    
    image = models.ImageField(upload_to='restaurants', verbose_name="Image", blank=True, null=True)
    
    admin_order_field = 'name'
    
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        app_label = 'restaurants'
        db_table = 'restaurants_restaurant'
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'
        
class Meal(models.Model):
    restaurant = models.ForeignKey(Restaurant, verbose_name="Restaurant")
    name = models.CharField(max_length=250, verbose_name="Nom")
    image = models.ImageField(upload_to='restaurants/meals', verbose_name="Image", blank=True, null=True)
    
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        app_label = 'restaurants'
        db_table = 'restaurants_meal'
        verbose_name = 'Repas'
        verbose_name_plural = 'Repas'

class MealTag(models.Model):
    tag = models.CharField(max_length=250, verbose_name="Tag")
    meals = models.ManyToManyField(Meal, verbose_name=u"Meals")
    
    class Meta:
        app_label = 'restaurants'
        db_table = 'restaurants_mealtag'
        verbose_name = 'Tag de repas'
        verbose_name_plural = 'Tag de repas'
    