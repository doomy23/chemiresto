# -*- coding: utf-8 -*-

from django.views.generic.base import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import DeleteView
import urlparse

from forms import *

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
        user = None
        form = RegistrationForm(data=request.POST)
        detailsForm = RegistrationDetailsForm(data=request.POST)
        
        if form.is_valid() and detailsForm.is_valid():
            user = form.save()
            group = Group.objects.get(id=1)
            user.groups.add(group)
            
            clientDetails = detailsForm.save(commit=False)
            clientDetails.user = user
            clientDetails.save()
            
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
        
        form = AuthenticationForm()
        
        request.session.set_test_cookie()
        
        return TemplateResponse(request, self.template_name, {'loginForm': form})
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if request.session.test_cookie_worked(): request.session.delete_test_cookie()
                
            redirect_to = request.GET.get('next', None)
        
            # Block redirections to other websites
            # and to the login/register page
            if redirect_to:
                netloc = urlparse.urlparse(redirect_to)[1]
                if netloc and netloc != request.get_host(): redirect_to = None
                if redirect_to == reverse('login'): redirect_to = None
                if redirect_to == reverse('register'): redirect_to = None
                
                if redirect_to: return HttpResponseRedirect(redirect_to)
                
            # Default redirection:
            # Look at the User's group and depending on if he's
            # a client or a guest, different redirection
            if not redirect_to: return user_default_redirect(user)
        
        return TemplateResponse(request, self.template_name, {'loginForm': form})

# Default redirection for a client depending on his groups
def user_default_redirect(user):
    groupNames = [x.name for x in user.groups.all()]
    
    if 'Client' in groupNames: return HttpResponseRedirect(reverse('manage_account'))
    elif 'Restaurateur' in groupNames: return HttpResponseRedirect('/admin/')
    else: return HttpResponseRedirect(reverse('home')) # Not supposed to happen
        
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
        
        return HttpResponseRedirect(reverse('login'))

# View used for
# /accounts/manage/
class ManagerView(View):
    template_name = 'accounts/manager.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try: userDetails = UserDetails.objects.get(user=request.user)
        except UserDetails.DoesNotExist: userDetails = None
        
        editAccountForm = EditAccountForm(instance=request.user)
        editAccountDetailsForm = EditAccountDetailsForm(instance=userDetails)
        passwordChangeForm = PasswordChangeForm(user=request.user)
        
        return TemplateResponse(request, self.template_name, {'editAccountForm':editAccountForm,
                                                              'editAccountDetailsForm':editAccountDetailsForm,
                                                              'passwordChangeForm':passwordChangeForm})
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try: userDetails = UserDetails.objects.get(user=request.user)
        except UserDetails.DoesNotExist: userDetails = None
        
        formSuccess = None
        formSuccessMessage = ""
        formName = request.POST.get('form-name')
        
        if formName == 'informations': 
            editAccountForm = EditAccountForm(instance=request.user, data=request.POST)
            editAccountDetailsForm = EditAccountDetailsForm(instance=userDetails, data=request.POST)
            
            if editAccountForm.is_valid():
                user = editAccountForm.save()
                editAccountForm = EditAccountForm(instance=user)
                
                if userDetails: editAccountDetailsForm.save()
                else:
                    # In case the userDetails does not exist yet
                    userDetails = editAccountDetailsForm.save(commit=False)
                    userDetails.user = user
                    userDetails.save()
                
                formSuccess = 'informations'
                formSuccessMessage = u"Vos informations de comptes ont été mises à jour avec succès."
            
        else:
            editAccountForm = EditAccountForm(instance=request.user)
            editAccountDetailsForm = EditAccountDetailsForm(instance=userDetails)
        
        if formName == 'password':
            passwordChangeForm = PasswordChangeForm(user=request.user, data=request.POST)
            
            if passwordChangeForm.is_valid():
                user = passwordChangeForm.save()
                passwordChangeForm = PasswordChangeForm(user=request.user)
                formSuccess = 'password'
                formSuccessMessage = u"Votre mot de passe a été modifié avec succès."
        
        else: passwordChangeForm = PasswordChangeForm(user=request.user)
        
        return TemplateResponse(request, self.template_name, {'formSuccess':formSuccess,
                                                              'formSuccessMessage':formSuccessMessage,
                                                              'editAccountForm':editAccountForm,
                                                              'editAccountDetailsForm':editAccountDetailsForm,
                                                              'passwordChangeForm':passwordChangeForm})

class DeleteView(DeleteView):
    model = User
    template_name = 'accounts/delete_account.html'
    success_url = reverse_lazy('login')
    
    # Overwrite of the delete function so that it does not
    # really delete the data but mark it as inactive
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        self.object.is_active = False
        self.object.save()
        
        logout(request)
        
        return HttpResponseRedirect(success_url)
