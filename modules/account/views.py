# -*- coding: utf-8 -*-

from django.views.generic.base import View
from django.template.response import TemplateResponse

class RegisterView(View):
    template_name = 'register.html'
    
    def get(self, request, *args, **kwargs):
        
        
        return TemplateResponse(request, self.template_name)
        