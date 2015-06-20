# -*- coding: utf-8 -*-

from django.core.urlresolvers import resolve

class CurrentPageMiddleware:
    def process_template_response(self, request, response):
        url = resolve(request.path_info)
        request.url_name = url.url_name
        request.url_namespaces = url.namespaces
        
        return response
    