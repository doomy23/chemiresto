# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Check if the user has access to the admin
def check_admin_right(user):
    return user.is_superuser

# Check if the user is a Restaurator
def check_restaurator_group(user):
    groupIds = [x.id for x in user.groups.all()]
    return 2 in groupIds

# Default redirection for a client depending on his groups
def user_default_redirect(user):
    groupIds = [x.id for x in user.groups.all()]
    
    if 1 in groupIds: return HttpResponseRedirect(reverse('accounts:manage_account'))
    elif 2 in groupIds: return HttpResponseRedirect(reverse('accounts:restaurators_dash'))
    else: return HttpResponseRedirect(reverse('home')) # Not supposed to happen

# Get the user type
def get_user_type(user):
    groupIds = [x.id for x in user.groups.all()]
    
    if 1 in groupIds: return 'Client'
    elif 2 in groupIds: return 'Restaurator'
    elif user.is_superuser: return 'Admin'
    else: return None