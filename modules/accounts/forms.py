# -*- coding: utf-8 -*-

import os

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import get_language, ugettext_lazy as _

from models import *

class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = _("Email")
    
    # Called before clean
    def clean_username(self):
        username = self.data['username']
        
        try:
            validate_email(username)
                
        except ValidationError:
            forms.ValidationError(_("Invalid email"))
        
        return username
        
class BaseUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        
    def __init__(self, *args, **kwargs):
        super(BaseUserForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        
    def clean_email(self):
        email = self.cleaned_data['email']
        
        users = User.objects.filter(email=email).count()
        if users > 0: raise forms.ValidationError(_("The email address you entered is already in use on another account"))

        return email
        
    def save(self, commit=True):
        instance = super(BaseUserForm, self).save(commit=False)
        instance.username = self.cleaned_data['email']
        if commit:
            instance.save()
        return instance

class RegistrationForm(BaseUserForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout('first_name', 'last_name', 'email', 'password1', 'password2')
    
class RegistrationDetailsForm(forms.ModelForm):
    conditions = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly', 'rows':'5'}))
    
    class Meta:
        model = UserDetails
        exclude = ("user",)
        
    def __init__(self, *args, **kwargs):
        super(RegistrationDetailsForm, self).__init__(*args, **kwargs)

        this_dir = os.path.dirname(__file__)
        rel_path = "../../licenses/license_%s.txt" % get_language()
        abs_file_path = os.path.join(this_dir, rel_path)
        
        try:
            license = open(abs_file_path, 'r').read()
        except:
            license = _("Unable to load the license at this time.")
            
        self.fields['conditions'].initial = license
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'tel', 'city', 'country', 'region', 'address1', 'address2', 'zip', 'conditions', 'consent_cp'
        )
        
    def clean_consent_cp(self):
        consent_cp = self.cleaned_data['consent_cp']
        
        if consent_cp == False: raise forms.ValidationError(_("You must accept"))
        
        return consent_cp

class EditAccountForm(BaseUserForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        
    def __init__(self, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.form_tag = False
    
class EditAccountDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        exclude = ("user", "consent_cp")
        
    def __init__(self, *args, **kwargs):
        super(EditAccountDetailsForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
            'tel', 'city', 'country', 'region', 'address1', 'address2', 'zip',
        )

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        exclude = ("user",)
        
    def __init__(self, *args, **kwargs):
        super(ShippingAddressForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
            'default', 'city', 'country', 'region', 'address1', 'address2', 'zip',
        )
        