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
from django.contrib import messages
import urllib

from accounts.models import UserAddress
from restaurant.models import Meal

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
        
        order_data = {
            'meals': {},
            'taxes': {},
            'taxes_total': 0,
            'taxable_subtotal': 0,
            'subtotal': 0,
            'total': 0
        }
        
        restaurant = None
        deliveryAddresses = UserAddress.objects.filter(user=request.user).order_by('-default')
        if deliveryAddresses: deliveryAddress = deliveryAddresses[0]
        else: deliveryAddress = None
        
        try:
            for k, v in request.GET.iteritems():
                meal = Meal.objects.get(id=k)
                    
                if not restaurant: restaurant = meal.menu.restaurant
                elif not restaurant == meal.menu.restaurant: raise Exception(_("Two or more selected meals are from different restaurants, this is technically impossible."))
                
                order_data['meals'][k] = {
                    'price': meal.price,
                    'taxable': meal.taxable,
                    'qte': v
                }
                
                cost = int(v) * meal.price
                order_data['subtotal'] += cost
                if meal.taxable: order_data['taxable_subtotal'] += cost
                
            # Calcul des taxes ici selon pays/region
            
            order_data['total'] = order_data['subtotal'] + order_data['taxes_total']

        except Exception as e:
            messages.error(self.request, _("Cannot create order: ")+unicode(e))
            order_data = None
            
        return TemplateResponse(request, self.template_name, {'order_data': order_data,
                                                              'restaurant':restaurant})
