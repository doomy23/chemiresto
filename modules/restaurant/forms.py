# -*- coding: utf-8 -*-

from django import forms
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from django.forms.formsets import formset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from extras.fields import COUNTRIES_LIST

from models import Meal, Menu, Restaurant

class RestaurantFilterForm(forms.Form):
    city = forms.CharField(label=_("city"), required=False)
    region = forms.CharField(label=_("state/province"), required=True)
    country = forms.ChoiceField(label=_("country"), required=True, choices=COUNTRIES_LIST)
    
    def __init__(self, *args, **kwargs):
        super(RestaurantFilterForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'country', 'region', 'city'
        )
        
class RestaurantForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RestaurantForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        
    def clean(self):
        cleaned_data = super(RestaurantForm, self).clean()
        
        if self.is_valid():
            name = cleaned_data.get("name")
            restaurateur = cleaned_data.get("restaurateur")
            
            if restaurateur:
                messages.success(self.request, _("'%s' was created successfully" % name))
            else:
                messages.warning(self.request, _("'%s' doesn't have a restaurateur" % name))
        
    class Meta:
        model = Restaurant
        fields = ['restaurateur', 'name', 'tel', 'city', 'region', 'country', 'address1', 'address2', 'zip',
            'image',]
        
class MenuForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        
    class Meta:
        model = Menu
        fields = ['name',]
        
class MealForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MealForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        
    def clean(self):
        cleaned_data = super(MealForm, self).clean()
        
        if self.is_valid():
            name = cleaned_data.get("name")
            description = cleaned_data.get("description")
            
            if description:
                messages.success(self.request, _("'%s' was created successfully" % name))
            else:
                messages.warning(self.request, _("'%s' doesn't have a description." % name))
        
    class Meta:
        model = Meal
        fields = ['name', 'description', 'price',]
        
MealsFormset = inlineformset_factory(Menu, Meal,
    form=MenuForm,
    formset=formset_factory(MealForm),
    extra=1)
