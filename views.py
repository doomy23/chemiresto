# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils import translation
from django.views.generic.base import TemplateView, View

class HomeView(View):
    http_method_names = [u'get',]
    
    def get(self, request, *args, **kwargs):
        # Redirige l'utilisateur selon son type. Si l'utilisateur est un
        # entrepreneur, un restaurateur ou un livreur, il est redirigé vers son
        # tableau de bord. S'il est un client ou un visiteur (utilisateur sans
        # compte), il est redirigé vers la liste des restaurants.
        redirect_to = None
        
        if request.user:
            if request.user.groups.filter(name="Entrepreneur").count():
                redirect_to = reverse('accounts:dashboard')
            if request.user.groups.filter(name="Restaurateur").count():
                redirect_to = reverse('accounts:dashboard')
            if request.user.groups.filter(name="Delivery man").count():
                redirect_to = reverse('accounts:dashboard')
                
        if not redirect_to:
            redirect_to = reverse('restaurant:restaurants_list')
        
        return HttpResponseRedirect(redirect_to)

class SelectLanguageView(TemplateView):
    template_name = "select_language.html"
    http_method_names = [u'get',]
    
    def get(self, request, *args, **kwargs):
        # Modifie la langue de la requête.
        
        if not self.kwargs['lang_code'] in dict(settings.LANGUAGES):
            raise Http404
        else:
            lang_code = self.kwargs['lang_code']
        
        if hasattr(request, 'session'):
            request.session['django_language'] = lang_code
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
        translation.activate(lang_code)
        
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
        