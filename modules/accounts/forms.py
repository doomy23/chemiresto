# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        
    def clean_email(self):
        email = self.cleaned_data['email']
        
        users = User.objects.filter(email=email).count()
        if users > 0: raise forms.ValidationError("Ce courriel est déjà utilisé")

        return email

class EditAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        
    def __init__(self, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        
    def clean_email(self):
        email = self.cleaned_data['email']
        
        if self.instance: users = User.objects.filter(email=email).exclude(id=self.instance.id).count()
        else : users = User.objects.filter(email=email).count()
        
        if users > 0: raise forms.ValidationError("Ce courriel est déjà utilisé")

        return email
        