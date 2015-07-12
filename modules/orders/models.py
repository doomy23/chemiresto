# -*- coding: utf-8 -*-

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from accounts.models import UserAddress
from restaurants.models import Restaurant
from extras.fields import CurrencyField

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, verbose_name=_("user"))
    restaurant = models.ForeignKey(Restaurant, verbose_name=_("restaurant"))
    
    total = CurrencyField(max_digits=10, decimal_places=2, verbose_name=_("cost before tax"))
    tips = CurrencyField(max_digits=10, decimal_places=2, verbose_name=_("tips"))
    taxable = models.BooleanField(verbose_name=_("taxable"))
    
    done = models.BooleanField(verbose_name=_("done"), default=False)
    delivered = models.BooleanField(verbose_name=_("delivered"), default=False)
    deliveryAddress = models.ForeignKey(UserAddress, verbose_name=_("delivery address"), null=True, blank=True)
    
    class Meta:
        app_label = 'orders'
        db_table = 'orders_order'
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
    
class OrderDetail(models.Model):
    #item = models.ForeignKey(MenuItem, verbose_name=u"Élément du menu")
    price = CurrencyField(max_digits=10, decimal_places=2, verbose_name=_("cost before tax"))
    qte = models.PositiveSmallIntegerField(verbose_name=_("qte"))
    taxable = models.BooleanField(verbose_name=_("taxable"), default=True)
    
    class Meta:
        app_label = 'orders'
        db_table = 'orders_orderdetail'
        verbose_name = 'Détails de commande'
        verbose_name_plural = 'Détails de commandes'
    
class OrderTax(models.Model):
    tax = models.CharField(max_length=10, verbose_name=_("tax"))
    rate = models.DecimalField(max_digits=5, decimal_places=4, verbose_name=_("rate"))
    price = CurrencyField(max_digits=10, decimal_places=2, verbose_name=_("price"))
    
    class Meta:
        app_label = 'orders'
        db_table = 'orders_ordertax'
        verbose_name = 'Taxe de commande'
        verbose_name_plural = 'Taxes de commandes'
    