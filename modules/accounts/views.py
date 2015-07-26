# -*- coding: utf-8 -*-

from django.views.generic.base import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group, User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import DeleteView
from django.views.generic.base import TemplateView
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib import messages
from decimal import Decimal
from datetime import datetime
import urlparse

from forms import *
from utils import *
from models import UserAddress, UserDetails

from orders.models import Order

# View used for
# /accounts/register/
class RegisterView(View):
    template_name = 'accounts/register.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated(): return user_default_redirect(request.user)
        
        user = None
        form = RegistrationForm()
        detailsForm = RegistrationDetailsForm()
        
        return TemplateResponse(request, self.template_name, {'registerForm': form,
                                                              'registerDetailsForm': detailsForm,
                                                              'user': user})
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated(): return user_default_redirect(request.user)
        
        user = None
        form = RegistrationForm(data=request.POST)
        detailsForm = RegistrationDetailsForm(data=request.POST)
        
        if form.is_valid() and detailsForm.is_valid():
            user = form.save()
            group = Group.objects.get(name="Client")
            user.groups.add(group)
            
            clientDetails = detailsForm.save(commit=False)
            clientDetails.user = user
            clientDetails.save()
            
            deliveryAddress = UserAddress()
            deliveryAddress.user = user
            deliveryAddress.default = True
            deliveryAddress.city = clientDetails.city
            deliveryAddress.region = clientDetails.region
            deliveryAddress.country = clientDetails.country
            deliveryAddress.address1 = clientDetails.address1
            deliveryAddress.address2 = clientDetails.address2
            deliveryAddress.zip = clientDetails.zip
            deliveryAddress.save()
            
            form = RegistrationForm()
        
        return TemplateResponse(request, self.template_name, {'registerForm': form,
                                                              'registerDetailsForm': detailsForm,
                                                              'user': user})

# View used for
# /accounts/login/
class LoginView(View):
    template_name = 'accounts/login.html'
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated(): return user_default_redirect(request.user)
        
        form = LoginForm()
        
        request.session.set_test_cookie()
        
        return TemplateResponse(request, self.template_name, {'loginForm': form})
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated(): return user_default_redirect(request.user)
        
        form = LoginForm(data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if request.session.test_cookie_worked(): request.session.delete_test_cookie()
            
            if user.id == 1: return HttpResponseRedirect(reverse('admin:index'))
            
            redirect_to = request.GET.get('next', None)
        
            # Block redirections to other websites
            # and to the login/register page
            if redirect_to:
                netloc = urlparse.urlparse(redirect_to)[1]
                if netloc and netloc != request.get_host(): redirect_to = None
                if redirect_to == reverse('accounts:login'): redirect_to = None
                if redirect_to == reverse('accounts:register'): redirect_to = None
                
                if redirect_to: return HttpResponseRedirect(redirect_to)
                
            # Default redirection:
            # Look at the User's group and depending on if he's
            # a client or a guest, different redirection
            if not redirect_to: return user_default_redirect(user)
        
        return TemplateResponse(request, self.template_name, {'loginForm': form})
        
# View used for
# /accounts/logout/
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        
        redirect_to = request.GET.get('next', None)
        
        if redirect_to:
            netloc = urlparse.urlparse(redirect_to)[1]
            if netloc and netloc != request.get_host(): redirect_to = None
            else: return HttpResponseRedirect(redirect_to)
        
        return HttpResponseRedirect(reverse('accounts:login'))

# View used for
# /accounts/dashboard/  
class DashboardView(View):
    template_name = "accounts/dashboard.html"
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        data = {}
        
        if request.user_details.is_a_client():
            data['unfinishedOrders'] = Order.objects.filter(user=request.user).exclude(state='DELIVERED')
            data['unpaidOrders'] = Order.objects.filter(user=request.user, paid=False)
            
        if request.user_details.is_a_restaurateur():
            nothingMoreToDoOnStates = ['READY', 'DELIVERING', 'DELIVERED']
            data['unfinishedOrders'] = Order.objects.filter(restaurant__restaurateur=request.user).exclude(state__in=nothingMoreToDoOnStates)
            data['deliveryOrders'] = Order.objects.filter(restaurant__restaurateur=request.user, state__in=['DELIVERING', 'READY'])
            data['unpaidOrders'] = Order.objects.filter(restaurant__restaurateur=request.user, state__in=nothingMoreToDoOnStates, paid=False)
            
        if request.user_details.is_a_delivery_man():
            try: data['currentlyDelivering'] = Order.objects.filter(state='DELIVERING', deliveryMan=request.user)[0]
            except: data['currentlyDelivering'] = None
            
            if not data['currentlyDelivering']:
                data['readyToDeliverOrders'] = Order.objects.filter(state="READY", deliveryMan=None)
        
        return TemplateResponse(request, self.template_name, data)
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        data = {}
        
        if request.user_details.is_a_delivery_man():
            try: data['currentlyDelivering'] = Order.objects.filter(state='DELIVERING', deliveryMan=request.user)[0]
            except: data['currentlyDelivering'] = None
            
            if not data['currentlyDelivering']:
                data['form_data'] = {
                    'errors':{},
                    'lat':request.POST.get('lat', ''),
                    'lon':request.POST.get('lon', ''),
                    'orderId':request.POST.get('order'),
                    'accept':request.POST.get('accept')
                }
                
                data['readyToDeliverOrders'] = Order.objects.filter(state="READY", deliveryMan=None)
                    
                try: 
                    lat = Decimal(data['form_data']['lat'])
                except: 
                    lat = None
                    data['form_data']['errors']['lat'] = True
                
                try: 
                    lon = Decimal(data['form_data']['lon'])
                except: 
                    lon = None
                    data['form_data']['errors']['lon'] = True
                
                if not data['form_data']['orderId']:
                    messages.error(self.request, _("You have to select one order before beginning."))
                    
                elif lat and lon:
                    try: 
                        order = Order.objects.get(id=data['form_data']['orderId'], state="READY", deliveryMan=None)
                    except:
                        order = None
                        messages.error(self.request, _("The selected order is no longer available."))
                    
                    if order:
                        #
                        # Affiche le trajet
                        # (possibilité d'accepter ou de revenir)
                        #
                        data['showDirectionsAndAccept'] = order
                        
                        if data['form_data']['accept']:
                            order.deliveryMan = request.user 
                            order.state = 'DELIVERING'
                            order.deliveryStart = datetime.now()
                            order.deliveryManLat = lat
                            order.deliveryManLon = lon
                            order.save()
                            
                            messages.success(self.request, _("The order state is now : DELIVERING"))
                            return HttpResponseRedirect(reverse('accounts:dashboard')) 
                        
            else:
                data['form_data'] = {
                    'errors':{},
                    'tips':request.POST.get('tips', 0),
                    'paid':request.POST.get('paid')
                }
                
                try: 
                    tips_value = Decimal(data['form_data']['tips']).quantize(Decimal('0.01'))
                    if tips_value < 0: data['form_data']['errors']['tips'] = True
                    
                except: data['form_data']['errors']['tips'] = True
                
                if len(data['form_data']['errors']) == 0:
                    data['currentlyDelivering'].state = 'DELIVERED'
                    data['currentlyDelivering'].deliveryEnd = datetime.now()
                    if data['form_data']['paid']: data['currentlyDelivering'].paid = True
                    if tips_value > 0: data['currentlyDelivering'].tips = tips_value
                    data['currentlyDelivering'].save()
                    
                    messages.success(self.request, _("You have completed a delivery successfully."))
                    return HttpResponseRedirect(reverse('accounts:dashboard')) 
            
        else:
            raise Http404
        
        return TemplateResponse(request, self.template_name, data)

# View used for
# /accounts/manage/
class ManagerView(View):
    template_name = 'accounts/manager.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try: userDetails = UserDetails.objects.get(user=request.user)
        except UserDetails.DoesNotExist: userDetails = None
        
        userAddresses = UserAddress.objects.filter(user=request.user)
        
        editAccountForm = EditAccountForm(instance=request.user)
        editAccountDetailsForm = EditAccountDetailsForm(instance=userDetails)
        passwordChangeForm = PasswordChangeForm(user=request.user)
        shippingForm = ShippingAddressForm()
        
        return TemplateResponse(request, self.template_name, {'userAddresses':userAddresses,
                                                              'editAccountForm':editAccountForm,
                                                              'editAccountDetailsForm':editAccountDetailsForm,
                                                              'passwordChangeForm':passwordChangeForm,
                                                              'shippingForm':shippingForm})
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try: userDetails = UserDetails.objects.get(user=request.user)
        except UserDetails.DoesNotExist: userDetails = None
        
        userAddresses = UserAddress.objects.filter(user=request.user)
        
        formSuccess = None
        formSuccessType = None
        formSuccessMessage = ""
        formName = request.POST.get('form-name')
        
        #
        # Informations form
        #
        if formName == 'informations': 
            editAccountForm = EditAccountForm(instance=request.user, data=request.POST)
            editAccountDetailsForm = EditAccountDetailsForm(instance=userDetails, data=request.POST)
            
            if (editAccountForm.is_valid() and not editAccountDetailsForm) or (editAccountForm.is_valid() and editAccountDetailsForm.is_valid()):
                user = editAccountForm.save()
                editAccountForm = EditAccountForm(instance=user)
                
                if userDetails and editAccountDetailsForm: editAccountDetailsForm.save()
                elif editAccountDetailsForm:
                    # In case the userDetails does not exist yet
                    userDetails = editAccountDetailsForm.save(commit=False)
                    userDetails.user = user
                    if not userDetails.id: userDetails.consent_cp = True
                    userDetails.save()
                
                formSuccess = 'informations'
                formSuccessMessage = _("Your account information has been successfully updated.")
            
        else:
            editAccountForm = EditAccountForm(instance=request.user)
            editAccountDetailsForm = EditAccountDetailsForm(instance=userDetails)
        
        #
        # Password form
        #
        if formName == 'password':
            passwordChangeForm = PasswordChangeForm(user=request.user, data=request.POST)
            
            if passwordChangeForm.is_valid():
                user = passwordChangeForm.save()
                passwordChangeForm = PasswordChangeForm(user=request.user)
                formSuccess = 'password'
                formSuccessMessage = _("Your password has been successfully updated.")
        
        else: passwordChangeForm = PasswordChangeForm(user=request.user)
        
        #
        # Shipping form
        #
        if formName == 'shipping':
            addressId = request.POST.get('id')
            delete = True if not request.POST.get('delete') == '0' else False
            
            try:
                address = UserAddress.objects.get(id=addressId, user=request.user)  if not addressId == '0' else None
                
                if not delete:
                    shippingForm = ShippingAddressForm(instance=address, data=request.POST)
                    
                    if shippingForm.is_valid():
                        if not address:
                            shippingAddress = shippingForm.save(commit=False)
                            shippingAddress.user = request.user
                            
                            if userAddresses.count() == 0 and shippingAddress.default == False: 
                                shippingAddress.default = True
                            elif userAddresses.count() > 0 and shippingAddress.default == True:
                                userAddresses.update(default=False)
                            
                            shippingAddress.save()
                            
                            formSuccess = 'shipping'
                            formSuccessType = 'success'
                            formSuccessMessage = _("The delivery address has been successfully created.")
                            
                            shippingForm = ShippingAddressForm()
                            
                        else:
                            unfinishedOrders = Order.objects.filter(user=request.user, deliveryAddress=address).exclude(state='DELIVERED')
                            
                            if unfinishedOrders.count() == 0:
                                shippingAddress = shippingForm.save(commit=False)
                                
                                if userAddresses.exclude(id=address.id).count() == 0 and shippingAddress.default == False: 
                                    shippingAddress.default = True
                                elif userAddresses.exclude(id=address.id).count() > 0 and shippingAddress.default == True:
                                    userAddresses.exclude(id=address.id).update(default=False)
                                    
                                shippingAddress.save()
                                
                                formSuccess = 'shipping'
                                formSuccessType = 'success'
                                formSuccessMessage = _("The delivery address has been successfully updated.")
                                
                                shippingForm = ShippingAddressForm()
                                
                            else:
                                formSuccess = 'shipping'
                                formSuccessType = 'danger'
                                formSuccessMessage = _("An unfinished command is associated with the delivery address.")
                            
                else:
                    shippingForm = ShippingAddressForm()
                    unfinishedOrders = Order.objects.filter(user=request.user, deliveryAddress=address).exclude(state='DELIVERED')
                    
                    if unfinishedOrders.count() == 0:
                        if userAddresses.exclude(id=address.id).count() > 0 and address.default:
                            firstUserAddressPossible = userAddresses.exclude(id=address.id)[0]
                            firstUserAddressPossible.default = True
                            firstUserAddressPossible.save()
                            
                        address.delete()
                        
                        formSuccess = 'shipping'
                        formSuccessType = 'success'
                        formSuccessMessage = _("The delivery address has been successfully deleted.")
                        
                    else:
                        formSuccess = 'shipping'
                        formSuccessType = 'danger'
                        formSuccessMessage = _("An unfinished command is associated with the delivery address.")
                
            except UserAddress.DoesNotExist:
                shippingForm = ShippingAddressForm()
                formSuccess = 'shipping'
                formSuccessType = 'danger'
                formSuccessMessage = _("The delivery address specified does not exist.")
            
        else: shippingForm = ShippingAddressForm()
        
        return TemplateResponse(request, self.template_name, {'userAddresses':userAddresses,
                                                              'formSuccess':formSuccess,
                                                              'formSuccessType':formSuccessType,
                                                              'formSuccessMessage':formSuccessMessage,
                                                              'editAccountForm':editAccountForm,
                                                              'editAccountDetailsForm':editAccountDetailsForm,
                                                              'passwordChangeForm':passwordChangeForm,
                                                              'shippingForm':shippingForm})

class DeleteUserView(DeleteView):
    model = User
    template_name = 'accounts/delete_account.html'
    success_url = reverse_lazy('accounts:login')
    
    # Overwrite of the confirmation page so that
    # it ensure the user is logged in and that he's not trying
    # to delete someone else
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        
        # Security check !
        if not self.object.id == request.user.id: raise Http404
        
        return self.render_to_response(context)
    
    # Overwrite of the delete function so that it does not
    # really delete the data but mark it as inactive
    @method_decorator(login_required)
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        # Security check !
        if not self.object.id == request.user.id: raise Http404
        
        self.object.is_active = False
        self.object.save()
        
        logout(request)
        
        return HttpResponseRedirect(success_url)
    