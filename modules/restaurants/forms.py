# -*- coding: utf-8 -*-

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django_countries.data import COUNTRIES

class RestaurantFilterForm(forms.Form):
    city = forms.CharField(label=u'Ville', required=False)
    region = forms.CharField(label=u'État/Province', required=True)
    country = forms.ChoiceField(label=u'Pays', required=True, choices=COUNTRIES)
    
    def __init__(self, *args, **kwargs):
        super(RestaurantFilterForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'country', 'region', 'city'
        )
        