# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from models import UserDetails

# Check if the user has access to the admin
def check_admin_right(user):
    return user.is_superuser

#
# The followings are no more used since anthony big refactoring
#

# Check if the user is a Restaurator
#def check_restaurator_group(user):
#    groupIds = [x.id for x in user.groups.all()]
#    return 2 in groupIds

# Default redirection for a client depending on his groups
def user_default_redirect(user):
    try: user_details = UserDetails.objects.get(user=user)
    except UserDetails.DoesNotExist: user_details = None
    
    if user_details:
        if user_details.is_an_entrepreneur() or user_details.is_a_restaurateur() or user_details.is_a_delivery_man():
            return HttpResponseRedirect(reverse('accounts:dashboard'))
        
    return HttpResponseRedirect(reverse('home'))

# Get the user type
#def get_user_type(user):
#    groupIds = [x.id for x in user.groups.all()]
#    
#    if 1 in groupIds: return 'Client'
#    elif 2 in groupIds: return 'Restaurator'
#    elif user.is_superuser: return 'Admin'
#    else: return None

