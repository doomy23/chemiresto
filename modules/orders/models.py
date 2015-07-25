# -*- coding: utf-8 -*-

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from accounts.models import UserAddress
from restaurant.models import Restaurant
from extras.fields import CurrencyField
from restaurant.models import Meal

ORDER_STATES = (
    ('UNFINISHED',_("unfinished")),
    ('AWAITING',_("awaiting")),
    ('DELIVERING',_("delivering")),
    ('DELIVERED',_("delivered")),
)

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, verbose_name=_("user"))
    restaurant = models.ForeignKey(Restaurant, verbose_name=_("restaurant"))
    
    total = CurrencyField(max_digits=10, decimal_places=2, verbose_name=_("cost before tax"))
    tips = CurrencyField(max_digits=10, decimal_places=2, verbose_name=_("tips"), default=0)
    
    state = models.CharField(verbose_name=_("state"), default='UNFINISHED', choices=ORDER_STATES, max_length=25)
    
    deliveryDatetime = models.DateTimeField(verbose_name=_("delivery datetime"))
    deliveryAddress = models.ForeignKey(UserAddress, verbose_name=_("delivery address"), null=True, blank=True)
    
    paypal_payment_id = models.TextField(null=True, blank=True)
    paypal_user_id = models.TextField(null=True, blank=True)
    paid = models.BooleanField(verbose_name=_("paid"), default=False)
    
    class Meta:
         app_label = 'orders'
    
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, verbose_name=_("order"))
    item = models.ForeignKey(Meal, verbose_name=_("meal"))
    price = CurrencyField(max_digits=10, decimal_places=2, verbose_name=_("cost before tax"))
    qte = models.PositiveSmallIntegerField(verbose_name=_("qte"))
    taxable = models.BooleanField(verbose_name=_("taxable"), default=True)
    
    class Meta:
         app_label = 'orders'
    
class OrderTax(models.Model):
    order = models.ForeignKey(Order, verbose_name=_("order"))
    tax = models.CharField(max_length=10, verbose_name=_("tax"))
    rate = models.DecimalField(max_digits=5, decimal_places=4, verbose_name=_("rate"))
    price = CurrencyField(max_digits=10, decimal_places=2, verbose_name=_("price"))
    
    class Meta:
         app_label = 'orders'
    