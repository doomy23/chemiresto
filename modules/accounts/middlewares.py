# -*- coding: utf-8 -*-

class AccountTypeMiddleware:
    def process_template_response(self, request, response):
        if request.user:
            request.user_type = self.get_user_type(request.user)
            
        return response
            
    # Get the user type from its groupnames
    def get_user_type(self, user):
        groupNames = [x.name for x in user.groups.all()]
        
        if 'Client' in groupNames: return 'Client'
        elif 'Restaurateur' in groupNames: return 'Restaurateur'
        else: return None
        