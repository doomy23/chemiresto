# -*- coding: utf-8 -*-

from django.views.generic.base import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages
from datetime import datetime
from decimal import Decimal
import urllib

from getenv import env
import paypalrestsdk

from accounts.models import UserAddress
from accounts.forms import ShippingAddressForm
from restaurant.models import Meal

from models import Order, OrderDetail, OrderTax, SUGGESTED_TIPS_RATE
from taxes import get_taxes_from

class OrderDetailView(View):
    template_name = 'orders/detail.html'
    order = None
    
    @method_decorator(login_required)
    def dispatch(self, request, id, *args, **kwargs):
        if request.user_details.is_a_client():
            try: self.order = Order.objects.get(id=id, user=request.user)
            except Order.DoesNotExist: raise Http404
            
            #
            # Payment execution
            #
            paymentId = request.GET.get('paymentId')
            payerID = request.GET.get('PayerID')
            
            if not self.order.paid and paymentId and payerID:
                paypalrestsdk.configure({
                    "mode": 'sandbox' if env('PAYPAL_SANDBOX') else 'live',
                    "client_id": env('PAYPAL_SANDBOX_CLIENT') if env('PAYPAL_SANDBOX') else env('PAYPAL_CLIENT'),
                    "client_secret": env('PAYPAL_SANDBOX_SECRET') if env('PAYPAL_SANDBOX') else env('PAYPAL_SECRET')
                })
                
                payment = paypalrestsdk.Payment.find(paymentId)
                
                if payment.execute({"payer_id": payerID}):
                    self.order.paypal_payment_id = paymentId
                    self.order.paypal_user_id = payerID
                    self.order.paid = True
                    self.order.paidDatetime = datetime.now()
                    self.order.save()
                    
                    messages.success(self.request, _("Thank you! You have paid your order successfully with PayPal."))
                    
                else:
                    messages.success(self.request, _("Impossible to proceed payment with PayPal : ") + unicode(payment.error))
            
        elif request.user_details.is_a_restaurateur():
            try: self.order = Order.objects.get(id=id, restaurant__restaurateur=request.user)
            except Order.DoesNotExist: raise Http404
            
        elif request.user_details.is_an_entrepreneur():
            try: self.order = Order.objects.get(id=id)
            except Order.DoesNotExist: raise Http404
            
        elif request.user_details.is_a_delivery_man():
            try: self.order = Order.objects.get(id=id, deliveryMan=None)
            except Order.DoesNotExist: raise Http404
            
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        nothingMoreToDoRestaurateurOnStates = ['READY', 'DELIVERING', 'DELIVERED']
        return TemplateResponse(request, self.template_name, {'order':self.order,
                                                              'nothingMoreToDoRestaurateurOnStates':nothingMoreToDoRestaurateurOnStates})
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form_data = {}
        form_name = request.POST.get('form-name')
        nothingMoreToDoRestaurateurOnStates = ['READY', 'DELIVERING', 'DELIVERED']
        
        #
        # Client actions
        #
        if request.user_details.is_a_client():
            if form_name == 'paypal' and not self.order.paid:
                form_data = {
                    'errors': {},
                    'tips': request.POST.get('tips')
                }
                
                try: 
                    tips_value = Decimal(form_data['tips']).quantize(Decimal('0.01'))
                    self.order.tips = tips_value
                    self.order.save()
                    
                    if tips_value < 0: form_data['errors']['tips'] = True
                    
                except: form_data['errors']['tips'] = True
                
                if len(form_data['errors']) == 0:
                    #
                    # Using PaypalSDK to create payment
                    #
                    paypalrestsdk.configure({
                        "mode": 'sandbox' if env('PAYPAL_SANDBOX') else 'live',
                        "client_id": env('PAYPAL_SANDBOX_CLIENT') if env('PAYPAL_SANDBOX') else env('PAYPAL_CLIENT'),
                        "client_secret": env('PAYPAL_SANDBOX_SECRET') if env('PAYPAL_SANDBOX') else env('PAYPAL_SECRET')
                    })
                    
                    payment_obj = {
                        "intent": "sale",
                        "payer": {
                            "payment_method": "paypal"
                        },
                        "redirect_urls": {
                            "return_url": request.build_absolute_uri(),
                            "cancel_url": request.build_absolute_uri()
                        },
                        "transactions": [{
                            "item_list": {
                                "items": []
                            },
                            "amount": {
                                "total": str(self.order.total + tips_value),
                                "currency": env('CURRENCY'),
                                "details": {
                                    "subtotal": str(self.order.subtotal + tips_value),
                                    "tax": str(self.order.tax_sum)
                                }
                            },
                            "description": "Payment of a Chemiresto's order"
                        }] 
                    }
                    
                    for detail in self.order.details:
                        payment_obj['transactions'][0]['item_list']['items'].append({
                            "name": detail.item.name,
                            "sku": detail.item.id,
                            "price": str(detail.price),
                            "currency": env('CURRENCY'),
                            "quantity": detail.qte
                        })
                        
                    if tips_value > 0:
                        payment_obj['transactions'][0]['item_list']['items'].append({
                            "name": 'TIPS',
                            "sku": 'TIPS',
                            "price": str(tips_value),
                            "currency": env('CURRENCY'),
                            "quantity": 1
                        })
                    
                    payment = paypalrestsdk.Payment(payment_obj)
                    
                    if payment.create():
                        for link in payment.links:
                            if link.method == "REDIRECT":
                                # Convert to str to avoid google appengine unicode issue
                                # https://github.com/paypal/rest-api-sdk-python/pull/58
                                redirect_url = str(link.href)
                                
                        return HttpResponseRedirect(redirect_url)
                        
                    else:
                        messages.error(self.request, _("Cannot create PayPal payment object : ") + unicode(payment.error))
                        
        #
        # Restaurateur actions
        #
        if request.user_details.is_a_restaurateur():
            
            if form_name == 'changestate-preparing' and self.order.state == 'AWAITING':
                self.order.state = 'PREPARING'
                self.order.save()
                messages.success(self.request, _("The order state has changed to : PREPARING"))
                
            if form_name == 'changestate-ready' and self.order.state == 'PREPARING':
                self.order.state = 'READY'
                self.order.save()
                messages.success(self.request, _("The order state has changed to : READY"))
        
        return TemplateResponse(request, self.template_name, {'order':self.order,
                                                              'form_data':form_data,
                                                              'nothingMoreToDoRestaurateurOnStates':nothingMoreToDoRestaurateurOnStates})

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
                order.subtotal = order_data['subtotal']
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
                
                messages.success(self.request, _("Your order has been created and you will be noticed as it changes state. You can pay on delivery or immediatly with Paypal. Your order number is : ") + str(order.id))
                return HttpResponseRedirect(reverse('accounts:dashboard'))
                
            except Exception as e:
                messages.error(self.request, _("Cannot create order: ")+unicode(e))
                
        return TemplateResponse(request, self.template_name, {'order_data': order_data,
                                                              'form_data':form_data,
                                                              'restaurant':restaurant,
                                                              'deliveryAddresses':deliveryAddresses,
                                                              'deliveryAddress':deliveryAddress,
                                                              'newShippingAddressForm':newShippingAddressForm})
        