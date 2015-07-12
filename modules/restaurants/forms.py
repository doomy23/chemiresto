# -*- coding: utf-8 -*-

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django_countries.data import COUNTRIES
from django.utils.translation import ugettext_lazy as _

class RestaurantFilterForm(forms.Form):
    city = forms.CharField(label=_("city"), required=False)
    region = forms.CharField(label=_("state/province"), required=True)
    country = forms.ChoiceField(label=_("country"), required=True, choices=COUNTRIES)
    
    def __init__(self, *args, **kwargs):
        super(RestaurantFilterForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'country', 'region', 'city'
        )
        