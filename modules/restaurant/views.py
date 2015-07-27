# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, UpdateView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

try: from django.contrib.gis.geoip import GeoIP
except: GeoIP = None

from models import Meal, Menu, Restaurant
from forms import MealForm, MenuForm, RestaurantFilterForm, RestaurantForm, RestaurantEditFilterForm

from accounts.mixins import AllowedGroupsMixin
from accounts.models import UserAddress

#
# Public Views
#
class RestaurantsView(View):
    template_name = 'restaurant/list.html'
    RESTAURANTS_BY_PAGE = 5
    
    def get(self, request, *args, **kwargs):
        if request.user_details and not request.user_details.is_a_client():
            return HttpResponseRedirect(reverse('accounts:dashboard'))
        
        pageNum = request.GET.get('p', 1)
        city = request.GET.get('city')
        region = request.GET.get('region')
        country = request.GET.get('country')
        
        #
        # By default takes user's default delivery address
        #
        if request.user.is_authenticated():
            deliveryAddresses = UserAddress.objects.filter(user=request.user).order_by('-default')
            
            if (not city or not region or not country) and deliveryAddresses:
                city = deliveryAddresses[0].city
                region = deliveryAddresses[0].region
                country = deliveryAddresses[0].country
        
        #
        # Otherwise takes the user_details location
        #
        if (not city or not region or not country) and \
            request.user.is_authenticated() and request.user_details:
            city = request.user_details.city
            region = request.user_details.region
            country = request.user_details.country
        
        #
        # GeoIp checkup to get the current city
        #
        elif (not city or not region or not country) and GeoIP:
            geoip = GeoIP()
            
            ip = request.META.get('REMOTE_ADDR')
            cityData = geoip.city(ip)
            
            if cityData:
                city = cityData.get('city')
                region = cityData.get('region')
                country = cityData.get('country_code')
        
        if (city and region and country) or (not city and region and country):
            filterForm = RestaurantFilterForm(data={'city':city,
                                                    'region':region,
                                                    'country':country})
        else: filterForm = RestaurantFilterForm()
        
        if city and region and country:
            objects = Restaurant.objects.filter(city=city, region=region, country=country).order_by('name')
        elif not city and region and country:
            objects = Restaurant.objects.filter(region=region, country=country).order_by('name')
        else:
            objects = Restaurant.objects.all().order_by('name')
        
        paginator = Paginator(objects, self.RESTAURANTS_BY_PAGE)
        
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

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurant/detail.html'
    context_object_name = 'restaurant'

#
# Entrepreneur Views
#
class RestaurantCreateView(AllowedGroupsMixin, CreateView):
    allowed_groups = ['Entrepreneur',]
    form_class = RestaurantForm
    template_name = 'restaurant/create.html'
    success_url = reverse_lazy('restaurant:restaurant_create')
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        if (form.is_valid()):
            name = form.cleaned_data.get("name")
            restaurateur = form.cleaned_data.get("restaurateur")
            
            if restaurateur:
                messages.success(self.request, _("'%s' has been successfully created" % name))
            else:
                messages.warning(self.request, _("'%s' has been successfully created but doesn't have an assigned restaurateur" % name))
                
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            
class RestaurantUpdateView(AllowedGroupsMixin, UpdateView):
    allowed_groups = ['Entrepreneur', ]
    form_class = RestaurantForm
    model = Restaurant
    success_url = reverse_lazy('restaurant:restaurant_list')
    template_name = 'restaurant/update.html'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        if (form.is_valid()):
            name = form.cleaned_data.get("name")
            restaurateur = form.cleaned_data.get("restaurateur")
            
            if restaurateur:
                messages.success(self.request, _("'%s' has been successfully updated" % name))
            else:
                messages.warning(self.request, _("'%s' has been successfully updated but doesn't have an assigned restaurateur" % name))
                
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
class RestaurantDeleteView(AllowedGroupsMixin, DeleteView):
    allowed_groups = ['Entrepreneur', ]
    model = Restaurant
    success_url = reverse_lazy('restaurant:restaurant_list')
    template_name = 'restaurant/delete.html'

class RestaurantListView(AllowedGroupsMixin, ListView):
    allowed_groups = ['Entrepreneur', ]
    context_object_name = 'restaurants'
    model = Restaurant
    template_name = 'restaurant/edit_list.html'
    
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        
        city = self.request.GET.get('city')
        region = self.request.GET.get('region')
        country = self.request.GET.get('country')
        
        filterForm = RestaurantEditFilterForm(data={'city':city, 'region':region, 'country':country})
            
        return self.render_to_response(
            self.get_context_data(filterForm=filterForm,))
    
    def get_queryset(self):
        city = self.request.GET.get('city')
        region = self.request.GET.get('region')
        country = self.request.GET.get('country')
        
        if not city and not region and not country:
            queryset = Restaurant.objects.all().order_by('name')
        else:
            if city and region and country:
                queryset = Restaurant.objects.filter(city=city, region=region, country=country).order_by('name')
            elif region and country:
                queryset = Restaurant.objects.filter(region=region, country=country).order_by('name')
            else:
                messages.error(self.request, _("You can search without a city, but the other fields are required."))
                queryset = Restaurant.objects.none()
            
        return queryset
    
#
# Restaurateur Views
#
class MenuCreateView(CreateView):
    template_name = 'restaurant/menus/create.html'
    form_class = MenuForm
    model = Menu
    success_url = reverse_lazy('restaurant:menu_list')
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        if (form.is_valid()):
            name = form.cleaned_data.get("name")
            messages.success(self.request, _("'%s' has been successfully created" % name))
                
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
class MenuListView(AllowedGroupsMixin, ListView):
    allowed_groups = ['Restaurateur', ]
    model = Menu
    template_name = 'restaurant/menus/list.html'
    
    def get_context_data(self, **kwargs):
        context = super(MenuListView, self).get_context_data(**kwargs)
        context['restaurants'] = Restaurant.objects.filter(restaurateur=self.request.user)
        return context

class MenuUpdateView(UpdateView):
    template_name = 'restaurant/menus/update.html'
    form_class = MenuForm
    model = Menu
    success_url = reverse_lazy('restaurant:menu_list')
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        if (form.is_valid()):
            name = form.cleaned_data.get("name")
            messages.success(self.request, _("'%s' has been successfully updated" % name))
                
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
class MealCreateView(CreateView):
    template_name = 'restaurant/menus/meal_create.html'
    form_class = MealForm
    model = Meal
    success_url = reverse_lazy('restaurant:menu_list')
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        if (form.is_valid()):
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            
            if description:
                messages.success(self.request, _("'%s' has been successfully created" % name))
            else:
                messages.warning(self.request, _("'%s' has been successfully created but doesn't have a description" % name))
                
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
class MealUpdateView(UpdateView):
    template_name = 'restaurant/menus/meal_update.html'
    form_class = MealForm
    model = Meal
    success_url = reverse_lazy('restaurant:menu_list')
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        if (form.is_valid()):
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            
            if description:
                messages.success(self.request, _("'%s' has been successfully updated" % name))
            else:
                messages.warning(self.request, _("'%s' has been successfully updated but doesn't have a description" % name))
                
            return self.form_valid(form)
        else:
            return self.form_invalid(form)