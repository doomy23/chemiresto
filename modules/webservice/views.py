# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import authentication, permissions, exceptions
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import simplejson
from django.contrib.auth.models import User
from datetime import datetime

class CustomSiteAuth(authentication.BaseAuthentication):
    email = ''
    passw = ''
    user = None
    user_details = None
    
    @csrf_exempt
    def authenticate(self, request):
        http_auth = request.META.get('HTTP_AUTHORIZATION', None)
        
        if http_auth:
            auth_string = http_auth[6:].decode('Base64')
            auth_table = auth_string.split(':')
            self.email = auth_table[0]
            self.passw = auth_table[1]
        
            try:
                self.user = User.objects.get(email=self.email)
                
                if self.user.check_password(self.passw): 
                    self.user_details = UserDetails.objects.get(user=self.user)
                    return ({'data':decode_data(request),}, self)
                else: 
                    raise exceptions.AuthenticationFailed('Permission denied 2')
                
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed('Permission denied 1')
            
        raise exceptions.AuthenticationFailed('Permission denied')

def decode_data(request):
    if request.POST:
        data_str = request.POST.get('data', None)
        return simplejson.loads(data_str.decode('Base64') if data_str else '{}')
        
    else:
        return None

@api_view(['POST'])
@authentication_classes((CustomSiteAuth,))
def test(request):
    
    return Response({"email": request.auth.email, "data_sent":request.user['data']})

from accounts.forms import EditAccountForm, EditAccountDetailsForm
from accounts.models import UserDetails

@api_view(['POST'])
@authentication_classes((CustomSiteAuth,))
def update_my_accounts(request):
    response = {
        'error': None,
        'results': []
    }
    
    data_sent = request.user['data']
    
    editAccountForm = EditAccountForm(data_sent, instance=request.auth.user)
    editAccountDetailsForm = EditAccountDetailsForm(data_sent, instance=request.auth.user_details)
    
    #if 
    
    return Response(response)
