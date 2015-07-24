# -*- coding: utf-8 -*-

from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from django.forms.formsets import formset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.forms.models import BaseInlineFormSet, inlineformset_factory
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
            'country', 'region', 'city', Submit('search', _("Search"))
        )
        
class RestaurantForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RestaurantForm, self).__init__(*args, **kwargs)
        self.fields['restaurateur'].queryset = User.objects.filter(groups__name='Restaurateur')
        self.helper = FormHelper()
        self.helper.form_tag = False
        
    class Meta:
        model = Restaurant
        fields = ['name', 'tel', 'country', 'region', 'city', 'address1', 'address2', 'zip', 'image', 'restaurateur']
        
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
        super(MealForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        
    class Meta:
        model = Meal
        fields = ['name', 'description', 'price',]
        
class MealBaseFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MealBaseFormSet, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        
    def clean(self):
        super(MealBaseFormSet, self).clean()
        
        for form in self.forms:
            if form.is_valid():
                name = form.cleaned_data.get("name")
                description = form.cleaned_data.get("description")
                
                if description:
                    messages.success(self.request, _("'%s' was created successfully" % name))
                else:
                    messages.warning(self.request, _("'%s' doesn't have a description." % name))
                    
MealFormset = inlineformset_factory(Menu, Meal,
    form=MealForm,
    formset=MealBaseFormSet,
    extra=2,
    can_delete=False,
)
