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
from decimal import Decimal
import urllib

from accounts.models import UserAddress
from restaurant.models import Meal

from taxes import get_taxes_from

SUGGESTED_TIPS_RATE = Decimal('0.15')

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
            'subtotal': 0,
            'taxable_subtotal': 0,
            'taxes': [],
            'taxes_total': 0,
            'total': 0,
            'suggested_tips': 0,
        }
        
        restaurant = None
        deliveryAddresses = UserAddress.objects.filter(user=request.user).order_by('-default')
        if deliveryAddresses: deliveryAddress = deliveryAddresses[0]
        else: deliveryAddress = None
        
        try:
            for mealId, qte in request.GET.iteritems():
                meal = Meal.objects.get(id=mealId)
                    
                if not restaurant: restaurant = meal.menu.restaurant
                elif not restaurant == meal.menu.restaurant: raise Exception(_("Two or more selected meals are from different restaurants, this is technically impossible."))
                
                cost = int(qte) * meal.price
                
                order_data['meals'][mealId] = {
                    'name': meal.name,
                    'price': meal.price,
                    'taxable': meal.taxable,
                    'qte': qte,
                    'cost': cost
                }
                
                order_data['subtotal'] += cost
                if meal.taxable: order_data['taxable_subtotal'] += cost
                
            #
            # Calcul des taxes ici selon pays/region
            #
            if deliveryAddress:
                order_data['taxes'] = get_taxes_from(deliveryAddress.country, deliveryAddress.region, order_data['taxable_subtotal'])
                for tax in order_data['taxes']: order_data['taxes_total'] += tax['amount']
            
            order_data['total'] = order_data['subtotal'] + order_data['taxes_total']
            order_data['suggested_tips'] = SUGGESTED_TIPS_RATE * order_data['total']

        except Exception as e:
            messages.error(self.request, _("Cannot create order: ")+unicode(e))
            order_data = None
            
        return TemplateResponse(request, self.template_name, {'order_data': order_data,
                                                              'restaurant':restaurant,
                                                              'deliveryAddresses':deliveryAddresses,
                                                              'deliveryAddress':deliveryAddress})
