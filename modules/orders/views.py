# -*- coding: utf-8 -*-

from django.views.generic.base import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext as _
import urllib

class OrderCreatorView(View):
    template_name = 'orders/create.html'
    
    def get(self, request, *args, **kwargs):
        # If not logged redirect to login with next as this exact page (with the GET)
        # So that after the login the user gets redirected here (doesnt work for a registration though)
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('accounts:login') + '?next=' + urllib.quote_plus(request.get_full_path()))
        
        # Only available to clients
        elif not request.user_details.is_a_client(): 
            return HttpResponseRedirect(request.user_details.get_default_redirect())
        
        
        
        return TemplateResponse(request, self.template_name, {})
