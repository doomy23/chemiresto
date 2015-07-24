# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _

class UserDetails(models.Model):
    user = models.OneToOneField(User, verbose_name=_("user"))
    birthdate = models.DateField(verbose_name=_("birth date"))
    tel = models.CharField(max_length=30, verbose_name=_("telephone"))
    city = models.CharField(max_length=250, verbose_name=_("city"))
    region = models.CharField(max_length=250, verbose_name=_("province/state/region"))
    country = CountryField(verbose_name=_("country"))
    address1 = models.CharField(max_length=250, verbose_name=_("address 1"))
    address2 = models.CharField(max_length=250, null=True, blank=True, verbose_name=_("address 2"))
    zip = models.CharField(max_length=10, verbose_name=_("zip code"))
    consent_cp = models.BooleanField(verbose_name=_("I agree to the Terms of Use, EULA and Privacy Policy"))
    
    def get_default_redirect(self):
        """
        Retourne la page vers laquelle l'utilisateur doit être rediriger selon
        sont type de compte.
        """
        if self.is_an_entrepreneur() or self.is_a_restaurateur() or self.is_a_delivery_man():
            redirect_to = reverse('accounts:dashboard')
        else:
            redirect_to = reverse('restaurant:restaurants')
            
        return redirect_to
        
    def is_an_entrepreneur(self):
        """
        Retourne VRAI si l'utilisateur est un entrepreneur.
        """
        return self.user.groups.filter(name='Entrepreneur').exists()
        
    def is_a_restaurateur(self):
        """
        Retourne VRAI si l'utilisateur est un restaurateur.
        """
        return self.user.groups.filter(name='Restaurateur').exists()
        
    def is_a_client(self):
        """
        Retourne VRAI si l'utilisateur est un client.
        """
        return self.user.groups.filter(name='Client').exists()
        
    def is_a_delivery_man(self):
        """
        Retourne VRAI si l'utilisateur est un livreur.
        """
        return self.user.groups.filter(name='Delivery man').exists()
    
    class Meta:
         app_label = 'accounts'
        
class UserAddress(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"))
    default = models.BooleanField(verbose_name=_("default delivery Address"))
    city = models.CharField(max_length=250, verbose_name=_("city"))
    region = models.CharField(max_length=250, verbose_name=_("province/state/region"))
    country = CountryField(verbose_name=_("country"))
    address1 = models.CharField(max_length=250, verbose_name=_("address 1"))
    address2 = models.CharField(max_length=250, null=True, blank=True, verbose_name=_("address 2"))
    zip = models.CharField(max_length=10, verbose_name=_("zip code"))
    
    class Meta:
         app_label = 'accounts'
    