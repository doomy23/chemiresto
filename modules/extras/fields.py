#
#    Class CurrencyField is from [Will Hardy]'s solution on Stackoverflow
#    http://stackoverflow.com/questions/2013835/django-how-should-i-store-a-money-value
#    edited Jun 11 '13 at 12:50 / answered Jan 6 '10 at 16:58 
#

from django.db import models
from decimal import Decimal

class CurrencyField(models.DecimalField):
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        try:
           return super(CurrencyField, self).to_python(value).quantize(Decimal("0.01"))
        except AttributeError:
           return None
       