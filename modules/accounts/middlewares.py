# -*- coding: utf-8 -*-

from utils import get_user_type

class AccountTypeMiddleware:
    def process_template_response(self, request, response):
        if request.user:
            request.user_type = get_user_type(request.user)
            
        return response
            