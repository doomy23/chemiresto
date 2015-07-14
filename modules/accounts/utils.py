# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

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
    
class AllowedGroupsMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.allowed_groups == '__all__':
            return super(AllowedGroupsMixin, self).dispatch(*args, **kwargs)
        else:
            allowed_groups = self.request.user.groups.values_list('name',flat=True)
            if [i for i in self.allowed_groups if i in allowed_groups]:
                return super(AllowedGroupsMixin, self).dispatch(*args, **kwargs)
            else:
                raise PermissionDenied
