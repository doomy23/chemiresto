# -*- coding: utf-8 -*-

from django.views.generic.base import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Check if the user has access to the admin
def check_admin_right(user):
    return user.is_staff

# Check if the user is a Restaurator
def check_restaurator_group(user):
    groupNames = [x.name for x in user.groups.all()]
    return 'Restaurateur' in groupNames

# ADMIN ONLY
# View used for
# /accounts/restaurators/create/
class CreateRestauratorView(View):
    template_name = 'accounts/create_restaurator.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if not check_admin_right(request.user): raise Http404()
        
        return TemplateResponse(request, self.template_name, {})
    