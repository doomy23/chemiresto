# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from models import UserDetails

class LoginForm(AuthenticationForm):
    is_using_email = None
    
    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = u"Courriel ou nom d'usagé"
    
    # Called before clean
    def clean_username(self):
        username = self.data['username']
        
        try:
            validate_email(username)
            self.is_using_email = username
            
            try:
                # Auth requires the username so we switch to it
                # And expect the password to be ok
                username = User.objects.get(email=username).username
                
            except ObjectDoesNotExist:
                raise ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username':self.username_field.verbose_name},
                )
                
        except ValidationError: pass
        
        return username
    
    # Overwrites AuthenticationForm clean method to support email address
    def clean(self):
        username = self.data['username']
        
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
                
            if self.user_cache is None:
                # If the auth is not ok and the user logged with an email
                # then we put back the email in case it was replaced in clean_username
                #
                # The main reason : Hackers could use this data leak as an opportunity to
                # fin credentials with bruteforce more easily by example...
                # @Doomy
                if self.is_using_email:
                    self.cleaned_data['username'] = self.is_using_email
                
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'first_name', 'last_name', 'email', 'username',
            HTML(u'''<a class="btn btn-primary" id="generate-username" onclick="RegisterForm.generateUsername()"><span class="fa fa-user"></span> Générer un nom automatiquement</a>'''),
            'password1', 'password2'
        )
        
    def clean_email(self):
        email = self.cleaned_data['email']
        
        users = User.objects.filter(email=email).count()
        if users > 0: raise forms.ValidationError("Ce courriel est déjà utilisé")

        return email
    
class RegistrationDetailsForm(forms.ModelForm):
    conditions = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly', 'rows':'5'}))
    save_as_delivery_address = forms.BooleanField(label=u"Enregistrer comme adresse de livraison", required=False, initial=True)
    
    class Meta:
        model = UserDetails
        exclude = ("user",)
        
    def __init__(self, *args, **kwargs):
        super(RegistrationDetailsForm, self).__init__(*args, **kwargs)
        
        self.fields['conditions'].initial = u'''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur massa ante, efficitur at elementum ut, faucibus at nisl. Duis vitae lectus molestie, commodo lectus sit amet, tempus risus. Duis posuere placerat mi quis placerat. Praesent diam nisl, scelerisque id urna eget, feugiat imperdiet turpis. Vivamus a nulla semper dolor commodo dignissim et ut nisl. Donec auctor porttitor orci, pretium sagittis quam molestie eu. Interdum et malesuada fames ac ante ipsum primis in faucibus. Morbi nisi ligula, rutrum tristique lacus eu, sollicitudin vehicula diam. Sed vehicula quis leo vel venenatis. Curabitur odio dui, feugiat vitae eros in, vestibulum venenatis sapien.

Etiam vitae augue semper, consequat eros vitae, venenatis ante. Donec ut tristique enim. Proin cursus nunc tortor, at mattis tortor rhoncus sed. Donec vehicula sem vitae tortor gravida viverra. Vestibulum bibendum aliquet turpis. In faucibus consectetur urna. Mauris tristique elementum dictum. Mauris ipsum justo, molestie vitae imperdiet a, posuere eu augue. Etiam aliquam ligula vel lacinia bibendum. Sed pharetra ornare elit mattis imperdiet. Ut dignissim urna nec sapien cursus sodales. Curabitur rhoncus, ex eget commodo pulvinar, enim est porttitor urna, maximus pellentesque nunc urna placerat erat. Ut id euismod ligula. Donec non nisi feugiat, venenatis ligula eget, cursus neque.

Aenean dictum lorem sapien, egestas blandit dui pharetra a. Suspendisse id dolor quis dui lobortis mollis quis a ante. Cras laoreet pretium quam, nec tempus lacus scelerisque vel. Nunc iaculis libero metus, ut hendrerit enim egestas eu. Nulla facilisi. Phasellus justo massa, hendrerit ac ullamcorper eget, porttitor non urna. Proin venenatis justo tempor efficitur pulvinar. Morbi quis mi lectus. 
'''
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'tel', 'city', 'country', 'region', 'address1', 'address2', 'zip', 'save_as_delivery_address', 'conditions', 'consent_cp'
        )
        
    def clean_consent_cp(self):
        consent_cp = self.cleaned_data['consent_cp']
        
        if consent_cp == False: raise forms.ValidationError("Vous devez consentir")
        
        return consent_cp

class EditAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        
    def __init__(self, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        
    def clean_email(self):
        email = self.cleaned_data['email']
        
        if self.instance: users = User.objects.filter(email=email).exclude(id=self.instance.id).count()
        else : users = User.objects.filter(email=email).count()
        
        if users > 0: raise forms.ValidationError("Ce courriel est déjà utilisé")

        return email
    
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
            'tel', 'city', 'country', 'region', 'address1', 'address2', 'zip', 'consent_cp'
        )
        