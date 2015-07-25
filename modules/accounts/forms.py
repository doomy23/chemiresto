# -*- coding: utf-8 -*-

import os

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import get_language, ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Submit

from models import UserAddress, UserDetails
from restaurant.models import Restaurant
        
class LoginForm(AuthenticationForm):
    # Formulaire de connexion des utilisateurs
    
    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = _("Email address")
    
    def clean_username(self):
        """
        Vérifie que l'adresse courriel saisie est valide. Sinon une erreur est levée.
        """
        username = self.data['username']
        
        try:
            validate_email(username)
                
        except ValidationError:
            forms.ValidationError(_("Invalid email address"))
        
        return username
        
class AbstractUserCreationForm(UserCreationForm):
    # Formulaire abstrait de création d'un utilisateur.
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        
    def __init__(self, *args, **kwargs):
        super(AbstractUserCreationForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        
    def clean_email(self):
        """
        Vérifie que l'adresse courriel saisie est valide et unique.
        Sinon une erreur est levée.
        """
        email = self.cleaned_data['email']
        
        users = User.objects.filter(email=email).count()
        if users > 0:
            raise forms.ValidationError(_("The email address you entered is already in use on another account"))
        
        return email
        
    def save(self, commit=True):
        """
        Enregistre le nouvel utilisateur.
        """
        instance = super(AbstractUserCreationForm, self).save(commit=False)
        
        # Il faut obligatoirement mettre un username pour que le modèle de base
        # de Django fonctionne alors on copie simplement l'adresse courriel.
        instance.username = self.cleaned_data['email']
        if commit:
            instance.save()
        return instance
        
class AbstractUserChangeForm(forms.ModelForm):
    # Formulaire abstrait de modification d'un utilisateur.
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        
    def __init__(self, *args, **kwargs):
        super(AbstractUserChangeForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        
    def save(self, commit=True):
        """
        Enregistre le nouvel utilisateur.
        """
        instance = super(AbstractUserChangeForm, self).save(commit=False)
        
        # Il faut obligatoirement mettre un username pour que le modèle de base
        # de Django fonctionne alors on copie simplement l'adresse courriel.
        instance.username = self.cleaned_data['email']
        if commit:
            instance.save()
        return instance

class RegistrationForm(AbstractUserCreationForm):
    # Formulaire concret de création d'un utilisateur.
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout('first_name', 'last_name', 'email', 'password1', 'password2')
    
class RegistrationDetailsForm(forms.ModelForm):
    # Formulaire pour enregistrer les détails d'un nouvel utilisateur.
    
    conditions = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly', 'rows':'5'}))
    
    class Meta:
        model = UserDetails
        exclude = ("user",)
        widgets = {
            'birthdate': forms.DateInput(attrs={'class':'datepicker'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(RegistrationDetailsForm, self).__init__(*args, **kwargs)

        # Charger la licence dans la langue préférée de l'utilisateur.
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
            'birthdate', 'tel', 'city', 'country', 'region', 'address1', 'address2', 'zip', 'conditions', 'consent_cp'
        )
        
    def clean_consent_cp(self):
        """
        Vérifie que l'utilisateur a bel et bien accepté les conditions d'utilisation du site.
        """
        consent_cp = self.cleaned_data['consent_cp']
        
        if consent_cp == False: raise forms.ValidationError(_("I agree to the Terms of Use, EULA and Privacy Policy"))
        
        return consent_cp

class EditAccountForm(AbstractUserChangeForm):
    # Formulaire concret de modification d'un utilisateur.
        
    def __init__(self, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
    
class EditAccountDetailsForm(forms.ModelForm):
    # Formulaire pour enregistrer les modifications des détails d'un utilisateur.
    
    class Meta:
        model = UserDetails
        exclude = ("user", "consent_cp")
        widgets = {
            'birthdate': forms.DateInput(attrs={'class':'datepicker'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(EditAccountDetailsForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        
        self.helper.layout = Layout(
            'birthdate', 'tel', 'city', 'country', 'region', 'address1', 'address2', 'zip',
        )

class ShippingAddressForm(forms.ModelForm):
    # Formulaire pour enregistrer une adresse de livraison.
    
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
            'city', 'country', 'region', 'address1', 'address2', 'zip',
        )
        
    def save(self, commit=True):
        """
        Enregistre la nouvelle adresse en tant qu'adresse par défaut.
        """
        instance = super(ShippingAddressForm, self).save(commit=False)
        
        instance.default = True
        if commit:
            instance.save()
        return instance
        
class CreateRestaurateurForm(AbstractUserCreationForm):
    # Formulaire pour créer un nouveau restaurateur.
    
    restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all(), label=_("Restaurant"), required=False)
    
    def __init__(self, *args, **kwargs):
        super(CreateRestaurateurForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'restaurant',
        )
        
class UpdateRestaurateurForm(AbstractUserChangeForm):
    # Formulaire pour enregistrer les modifications faites à un restaurateur.
    
    restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all(), label=_("Restaurant"), required=False)
    
    def __init__(self, *args, **kwargs):
        super(UpdateRestaurateurForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'first_name', 'last_name', 'email', 'username', 'restaurant',
        )
        
