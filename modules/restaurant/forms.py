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
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

from extras.fields import COUNTRIES_LIST

from models import Meal, Menu, Restaurant

class UserFullnameChoiceField(forms.ModelChoiceField):
    # Champ de sélection des utilisateurs par leur nom complet.
    
    def label_from_instance(self, obj):
        return smart_unicode(obj.get_full_name())
        
class RestaurantFilterForm(forms.Form):
    city = forms.CharField(label=_("city"), required=False)
    region = forms.CharField(label=_("state/province"), required=True)
    country = forms.ChoiceField(label=_("country"), required=True, choices=COUNTRIES_LIST)
    
    def __init__(self, *args, **kwargs):
        super(RestaurantFilterForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'country', 'region', 'city', Submit('search', _("Search"), css_class="btn-success")
        )
        
class RestaurantEditFilterForm(forms.Form):
    city = forms.CharField(label=_("city"), required=False)
    region = forms.CharField(label=_("state/province"), required=False)
    country = forms.ChoiceField(label=_("country"), required=False, choices=COUNTRIES_LIST)
    
    def __init__(self, *args, **kwargs):
        super(RestaurantEditFilterForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'country', 'region', 'city', Submit('search', _("Search"))
        )
        
class RestaurantForm(ModelForm):
    restaurateur = UserFullnameChoiceField(queryset=User.objects.all())

    def __init__(self, *args, **kwargs):
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
        fields = '__all__'
        
class MealBaseFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MealBaseFormSet, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
                    
MealFormset = inlineformset_factory(Menu, Meal,
    form=MealForm,
    formset=MealBaseFormSet,
    extra=1,
    can_delete=False,
)
