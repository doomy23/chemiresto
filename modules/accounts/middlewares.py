# -*- coding: utf-8 -*-

from models import UserDetails
from utils import get_user_type

class AccountTypeMiddleware:
    def process_request(self, request):
        if request.user:
            request.user_type = get_user_type(request.user)
            try: request.user_details = UserDetails.objects.get(user=request.user)
            except: request.user_details = None
            
        return
            