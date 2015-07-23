# -*- coding: utf-8 -*-

from django.views.generic.base import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext as _
from django.views.generic.list import ListView

from restaurator_forms import *
from utils import *

# ADMIN ONLY
# View used for
# /accounts/restaurators/create/
class CreateRestauratorView(View):
    template_name = 'accounts/create_restaurator.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if not request.user_details.is_an_entrepreneur(): raise Http404()
        
        form = CreateRestauratorForm()
        
        return TemplateResponse(request, self.template_name, {'form':form})
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if not request.user_details.is_an_entrepreneur(): raise Http404()
        
        messageType = None
        message = ""
        
        form = CreateRestauratorForm(request.POST)
        
        if form.is_valid():
            group = Group.objects.get(id=2)
            
            restaurant = form.cleaned_data['restaurant']
            restaurator = form.save()
            restaurator.groups.add(group)
            
            if restaurant:
                restaurant.user = restaurator
                restaurant.save()
                
                messageType = "success"
                message = _("The restaurateur was successfully created its restaurant has been assigned.")
            
            else:
                messageType = "warning"
                message = _("The restaurateur was successfully created but he doesn't have any associated restaurant.")
            
            form = CreateRestauratorForm()
        
        return TemplateResponse(request, self.template_name, {'form':form,
                                                              'message':message,
                                                              'messageType':messageType})
    
# View used for
# /accounts/restaurators/
class RestauratorDashView(View):
    template_name = 'accounts/restaurator_dash.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if not check_restaurator_group(request.user): raise Http404()
        
        return TemplateResponse(request, self.template_name, {})

class RestauratorListView(ListView):
    model = User
    context_object_name = 'restaurateurs'
    #queryset = User.objects.filter(groups__name='Restaurateur')
    template_name = 'accounts/restaurator_list.html'
