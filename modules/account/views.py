# -*- coding: utf-8 -*-

from django.views.generic.base import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
import urlparse

# View used for
# /account/register/
class RegisterView(View):
    template_name = 'account/register.html'
    
    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, self.template_name)

# View used for
# /account/login/
class LoginView(View):
    template_name = 'account/login.html'
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def get(self, request, *args, **kwargs):
        # Redirect user if authenticated
        if request.user.is_authenticated(): 
            return self.user_default_redirect(request.user)
        
        form = AuthenticationForm()
        
        request.session.set_test_cookie()
        
        return TemplateResponse(request, self.template_name, {
                'loginForm': form
            })
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if request.session.test_cookie_worked(): request.session.delete_test_cookie()
                
            redirect_to = request.GET.get('redirect_to', None)
        
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
            if not redirect_to: return self.user_default_redirect(user)
        
        return TemplateResponse(request, self.template_name, {
                'loginForm': form
            })
    
    def user_default_redirect(self, user):
        groupNames = [x.name for x in user.groups.all()]
        
        if 'Client' in groupNames:
            return HttpResponseRedirect(reverse('home'))
        
        elif 'Restaurateur' in groupNames:
            return HttpResponseRedirect('/admin/')
        
        else:
            # Not supposed to happen
            return HttpResponseRedirect(reverse('home'))
        
# View used for
# /account/logout/
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        
        redirect_to = request.GET.get('redirect_to', None)
        
        if redirect_to:
            netloc = urlparse.urlparse(redirect_to)[1]
            if netloc and netloc != request.get_host(): redirect_to = None
            else: return HttpResponseRedirect(redirect_to)
        
        return HttpResponseRedirect(reverse('login'))
        