# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit
from django.utils.translation import ugettext_lazy as _

from restaurants.models import Restaurant

class CreateRestauratorForm(UserCreationForm):
    restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all(), label=_("Assign a restaurant"), required=False)
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        
    def __init__(self, *args, **kwargs):
        super(CreateRestauratorForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'first_name', 'last_name', 'email', 'username',
            HTML(u'''<a class="btn btn-primary" id="generate-username" onclick="RegisterForm.generateUsername()"><span class="fa fa-user"></span> Générer un nom automatiquement</a>'''),
            'password1', 'password2', 'restaurant',
            Submit('create', _("Create the restaurateur"), css_class='btn btn-primary')
        )
        
    def clean_email(self):
        email = self.cleaned_data['email']
        
        users = User.objects.filter(email=email).count()
        if users > 0: raise forms.ValidationError(_("This email address is already in use."))

        return email