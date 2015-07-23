# -*- coding: utf-8 -*-

from models import UserDetails

class AccountTypeMiddleware:
    def process_request(self, request):
        if request.user:
            try: request.user_details = UserDetails.objects.get(user=request.user)
            except: request.user_details = None
            
        return
            