# -*- coding: utf-8 -*-
from django.views.generic.base import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseForbidden

try: from django.contrib.gis.geoip import GeoIP
except: GeoIP = None

from models import Restaurant
from forms import *
from accounts.utils import AllowedGroupsMixin

RESTAURANTS_BY_PAGE = 1

class RestaurantCreateView(AllowedGroupsMixin, SuccessMessageMixin, CreateView):
    model = Restaurant
    fields = ('name', 'tel', 'city', 'region', 'country', 'address1', 'address2', 'zip', 'user')
    template_name = 'restaurants/create.html'
    success_message = _("%(name)s was created successfully")
    allowed_groups = ('Entrepreneur',)
    
    def form_valid(self, form):
        if not form.cleaned_data['user']:
            messages.warning(self.request, _("You have just created a new restaurant without assign it a restaurateur."))
        return super(RestaurantCreateView, self).form_valid(form)  
    
    def get_success_url(self):
        return reverse('restaurants:restaurants_details',args=(self.object.id,))

class RestaurantsView(View):
    template_name = 'restaurants/list.html'
    
    def get(self, request, *args, **kwargs):
        pageNum = request.GET.get('p', 1)
        city = request.GET.get('city')
        region = request.GET.get('region')
        country = request.GET.get('country')
        
        if (not city or not region or not country) and \
            request.user and request.user_details:
            city = request.user_details.city
            region = request.user_details.region
            country = request.user_details.country
            
        elif (not city or not region or not country) and GeoIP:
            geoip = GeoIP()
            
            ip = request.META.get('REMOTE_ADDR')
            cityData = geoip.city(ip)
            
            if cityData:
                city = cityData.get('city')
                region = cityData.get('region')
                country = cityData.get('country_code')
                
        filterForm = RestaurantFilterForm(data={'city':city,
                                                'region':region,
                                                'country':country})
        
        if city and region and country:
            objects = Restaurant.objects.filter(city=city, region=region, country=country).order_by('name')
        else:
            objects = Restaurant.objects.all().order_by('name')
        
        paginator = Paginator(objects, RESTAURANTS_BY_PAGE)
        
        try:
            page = paginator.page(pageNum)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        
        return TemplateResponse(request, self.template_name, {'page':page,
                                                              'paginator':paginator,
                                                              'city':city,
                                                              'region':region,
                                                              'country':country,
                                                              'filterForm':filterForm})

class RestaurantsDetailsView(View):
    template_name = 'restaurants/details.html'
    
    def get(self, request, id, *args, **kwargs):
        try: restaurant = Restaurant.objects.get(id=id)
        except Restaurant.DoesNotExist: raise Http404
        
        return TemplateResponse(request, self.template_name, {'restaurant':restaurant})
