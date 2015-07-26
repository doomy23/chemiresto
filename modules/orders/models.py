# -*- coding: utf-8 -*-

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from extras.utilities import get_tuple_value
from accounts.models import UserAddress
from restaurant.models import Restaurant
from extras.fields import CurrencyField
from restaurant.models import Meal
from decimal import Decimal

SUGGESTED_TIPS_RATE = Decimal('0.15')

ORDER_STATES = (
    ('AWAITING',_("awaiting")),
    ('PREPARING',_("preparing")),
    ('READY',_("ready")),
    ('DELIVERING',_("delivering")),
    ('DELIVERED',_("delivered")),
)

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, verbose_name=_("user"))
    deliveryMan = models.ForeignKey(User, verbose_name=_("delivery man"), null=True, blank=True, related_name="delivery_man")
    restaurant = models.ForeignKey(Restaurant, verbose_name=_("restaurant"))
    
    subtotal = CurrencyField(max_digits=10, decimal_places=2, verbose_name=_("cost before tax"))
    total = CurrencyField(max_digits=10, decimal_places=2, verbose_name=_("cost after tax"))
    tips = CurrencyField(max_digits=10, decimal_places=2, verbose_name=_("tips"), default=0)
    
    state = models.CharField(verbose_name=_("state"), default='AWAITING', choices=ORDER_STATES, max_length=25)
    
    deliveryDatetime = models.DateTimeField(verbose_name=_("delivery datetime"))
    deliveryAddress = models.ForeignKey(UserAddress, verbose_name=_("delivery address"), null=True, blank=True)
    deliveryStart = models.DateTimeField(verbose_name=_("delivery start"), null=True, blank=True)
    deliveryEnd = models.DateTimeField(verbose_name=_("delivery end"), null=True, blank=True)
    deliveryManLat = models.FloatField(null=True, blank=True)
    deliveryManLon = models.FloatField(null=True, blank=True)
    
    paypal_payment_id = models.TextField(null=True, blank=True)
    paypal_user_id = models.TextField(null=True, blank=True)
    paid = models.BooleanField(verbose_name=_("paid"), default=False)
    paidDatetime = models.DateTimeField(verbose_name=_("paid datetime"), null=True, blank=True)
    
    @property
    def id_as_string(self):
        return str(self.id)
    
    @property
    def suggested_tips(self):
        return SUGGESTED_TIPS_RATE * self.total
    
    @property
    def get_state_text(self):
        return get_tuple_value(ORDER_STATES, self.state)
    
    @property
    def details(self):
        return OrderDetail.objects.filter(order=self)
    
    @property
    def taxes(self):
        return OrderTax.objects.filter(order=self)
    
    @property
    def tax_sum(self):
        sum = 0
        for tax in self.taxes: sum += tax.price
        return sum
    
    class Meta:
         app_label = 'orders'
    
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, verbose_name=_("order"))
    item = models.ForeignKey(Meal, verbose_name=_("meal"))
    price = CurrencyField(max_digits=10, decimal_places=2, verbose_name=_("cost before tax"))
    qte = models.PositiveSmallIntegerField(verbose_name=_("qte"))
    taxable = models.BooleanField(verbose_name=_("taxable"), default=True)
    
    @property
    def cost(self):
        return self.price * self.qte
    
    class Meta:
         app_label = 'orders'
    
class OrderTax(models.Model):
    order = models.ForeignKey(Order, verbose_name=_("order"))
    tax = models.CharField(max_length=10, verbose_name=_("tax"))
    rate = models.DecimalField(max_digits=5, decimal_places=4, verbose_name=_("rate"))
    price = CurrencyField(max_digits=10, decimal_places=2, verbose_name=_("price"))
    
    class Meta:
         app_label = 'orders'
    