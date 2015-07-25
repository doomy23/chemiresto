# -*- coding: utf-8 -*-

from django.views.generic.base import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages
from datetime import datetime
from decimal import Decimal
import urllib

from accounts.models import UserAddress
from accounts.forms import ShippingAddressForm
from restaurant.models import Meal

from models import Order, OrderDetail, OrderTax
from taxes import get_taxes_from

SUGGESTED_TIPS_RATE = Decimal('0.15')

class OrderCreatorView(View):
    template_name = 'orders/create.html'
    
    def dispatch(self, request, *args, **kwargs):
        # If not logged redirect to login with next as this exact page (with the GET)
        # So that after the login the user gets redirected here (doesnt work for a registration though)
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('accounts:login') + '?next=' + urllib.quote_plus(request.get_full_path()))
        
        # Only available to clients
        elif not request.user_details.is_a_client(): 
            return HttpResponseRedirect(request.user_details.get_default_redirect())
            
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
    
    def build_order_data(self, request, deliveryAddress):
        restaurant = None
        
        order_data = {
            'meals': {},
            'subtotal': 0,
            'taxable_subtotal': 0,
            'taxes': [],
            'taxes_total': 0,
            'total': 0,
            'suggested_tips': 0,
        }
        
        for mealId, qte in request.GET.iteritems():
            meal = Meal.objects.get(id=mealId)
                
            if not restaurant: restaurant = meal.menu.restaurant
            elif not restaurant == meal.menu.restaurant: raise Exception(_("Two or more selected meals are from different restaurants, this is technically impossible."))
            
            cost = int(qte) * meal.price
            
            order_data['meals'][mealId] = {
                'obj': meal,
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
        
        return order_data, restaurant
    
    def get(self, request, *args, **kwargs):
        restaurant = None
        deliveryAddresses = UserAddress.objects.filter(user=request.user).order_by('-default')
        if deliveryAddresses: deliveryAddress = deliveryAddresses[0]
        else: deliveryAddress = None
        
        try:
            order_data, restaurant = self.build_order_data(request, deliveryAddress)
            newShippingAddressForm = ShippingAddressForm()

        except Exception as e:
            messages.error(self.request, _("Cannot create order: ")+unicode(e))
            order_data = None
            
        return TemplateResponse(request, self.template_name, {'order_data': order_data,
                                                              'restaurant':restaurant,
                                                              'deliveryAddresses':deliveryAddresses,
                                                              'deliveryAddress':deliveryAddress,
                                                              'newShippingAddressForm':newShippingAddressForm})
        
    def post(self, request, *args, **kwargs):
        restaurant = None
        deliveryAddress = None
        deliveryAddresses = UserAddress.objects.filter(user=request.user).order_by('-default')
        
        form_data = {
            'delivery_address': request.POST.get('delivery_address', ''),
            'new_delivery_address': {
                'country': request.POST.get('country', ''),
                'region': request.POST.get('region', ''),
                'city': request.POST.get('city', ''),
                'address1': request.POST.get('address1', ''),
                'address2': request.POST.get('address2', ''),
                'zip': request.POST.get('zip', '')
            },
            'show_new_delivery_addr_form': False,
            'delivery_datetime': request.POST.get('delivery_datetime', ''),
            'errors': {},
            'has_errors': False
        }
        
        if not form_data['new_delivery_address']['country'].strip() == "" or not form_data['new_delivery_address']['region'].strip() == "" or \
            not form_data['new_delivery_address']['city'].strip() == "" or not form_data['new_delivery_address']['address1'].strip() == "" or \
            not form_data['new_delivery_address']['address2'].strip() == "" or not form_data['new_delivery_address']['zip'].strip() == "":
            #
            # New delivery address creation
            #
            newShippingAddressForm = ShippingAddressForm(request.POST)
            
            if newShippingAddressForm.is_valid():
                newShippingAddress = newShippingAddressForm.save(commit=False)
                newShippingAddress.user = request.user
                
                if deliveryAddresses.count() == 0 and newShippingAddress.default == False: 
                    newShippingAddress.default = True
                elif deliveryAddresses.count() > 0 and newShippingAddress.default == True:
                    deliveryAddresses.update(default=False)
                
                newShippingAddress.save()
                deliveryAddresses = UserAddress.objects.filter(user=request.user).order_by('-default')
                deliveryAddress = newShippingAddress
                form_data['delivery_address'] = deliveryAddress.id
                
                newShippingAddressForm = ShippingAddressForm()
                
            else:
                form_data['show_new_delivery_addr_form'] = True
                form_data['has_errors'] = True
                
                if deliveryAddresses: 
                    deliveryAddress = deliveryAddresses[0]
                    form_data['delivery_address'] = deliveryAddress.id
            
        else:
            #
            # Getting delivery address from select
            #
            newShippingAddressForm = ShippingAddressForm()
            
            try:
                deliveryAddress = UserAddress.objects.get(id=form_data['delivery_address'], user=request.user)
                form_data['delivery_address'] = deliveryAddress.id
                
            except:
                form_data['errors']['delivery_address'] = _("Missing delivery address")
                form_data['has_errors'] = True
                
        try:
            order_data, restaurant = self.build_order_data(request, deliveryAddress)

        except Exception as e:
            messages.error(self.request, _("Cannot create order: ")+unicode(e))
            order_data = None
            
        #
        # Validating delivery datetime
        #
        try:
            deliveryDatetime = datetime.strptime(form_data['delivery_datetime'], '%Y-%m-%d %H:%M:%S')
            
        except:
            deliveryDatetime = None
            form_data['errors']['delivery_datetime'] = _("Invalid datetime format")
            
        #
        # Finalisation
        #
        if order_data and not form_data['has_errors'] and deliveryDatetime and deliveryAddress:
            try:
                order = Order()
                order.user = request.user
                order.restaurant = restaurant
                order.total = order_data['total']
                order.state = 'AWAITING'
                order.deliveryAddress = deliveryAddress
                order.deliveryDatetime = deliveryDatetime
                order.save()
                
                for mealId, meal in order_data['meals'].iteritems():
                    orderDetail = OrderDetail()
                    orderDetail.order = order
                    orderDetail.item = meal['obj']
                    orderDetail.price = meal['price']
                    orderDetail.qte = meal['qte']
                    orderDetail.taxable = meal['taxable']
                    orderDetail.save()
                    
                for tax in order_data['taxes']:
                    orderTax = OrderTax()
                    orderTax.order = order
                    orderTax.tax = tax['tax']
                    orderTax.rate = tax['rate']
                    orderTax.price = tax['amount']
                    orderTax.save()
                
                messages.success(self.request, _("Your order has been created and you will be noticed as it changes state. You can pay on delivery on immediatly via Paypal."))
                return HttpResponseRedirect(reverse('accounts:dashboard'))
                
            except Exception as e:
                messages.error(self.request, _("Cannot create order: ")+unicode(e))
                
        return TemplateResponse(request, self.template_name, {'order_data': order_data,
                                                              'form_data':form_data,
                                                              'restaurant':restaurant,
                                                              'deliveryAddresses':deliveryAddresses,
                                                              'deliveryAddress':deliveryAddress,
                                                              'newShippingAddressForm':newShippingAddressForm})
        