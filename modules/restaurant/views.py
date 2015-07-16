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
from django.views.generic import DetailView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, DeleteView
from django.shortcuts import get_object_or_404

try: from django.contrib.gis.geoip import GeoIP
except: GeoIP = None

from models import Meal, Menu, Restaurant
from forms import MealFormset, MenuForm, RestaurantFilterForm, RestaurantForm

class RestaurantCreateView(CreateView):
    template_name = 'restaurants/create.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="Entrepreneur").exists():
            # Seul un entrepreneur peut créer un restaurant
            return HttpResponseForbidden()
            
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
        
    def get(self, request, *args, **kwargs):
        self.object = None
        form = RestaurantForm(request=request)
        return self.render_to_response(
            self.get_context_data(form=form,))
                                  
    def get_success_url(self):
        return reverse('restaurant:restaurant_detail', kwargs={'pk': self.object.pk})
        
    def post(self, request, *args, **kwargs):
        self.object = None
        form = RestaurantForm(self.request.POST, request=request)
        if (form.is_valid()):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            
class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurants/detail.html'
    
class RestaurantDeleteView(DeleteView):
    model = Restaurant
    success_url = reverse_lazy('restaurant:restaurant_list')
    template_name = 'restaurants/delete.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="Entrepreneur").exists():
            # Seul un entrepreneur peut supprimer un restaurant
            return HttpResponseForbidden()
            
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
    
class RestaurantListView(View):
    template_name = 'restaurants/list.html'
    RESTAURANTS_BY_PAGE = 1
    
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
        
        if city and region and country:
            filterForm = RestaurantFilterForm(data={'city':city,
                                                    'region':region,
                                                    'country':country})
        else: filterForm = RestaurantFilterForm()
        
        if city and region and country:
            objects = Restaurant.objects.filter(city=city, region=region, country=country).order_by('name')
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

class MenuCreateView(CreateView):
    template_name = 'restaurants/menus/create.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user == self.get_restaurant().restaurateur:
            # Seul le restaurateur qui possède le restaurant peut modifier le
            # menu.
            return HttpResponseForbidden()
            
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def form_invalid(self, form, meal_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  meal_formset=meal_formset,))
        
    def form_valid(self, form, meal_formset):
        self.object = form.save(commit=False)
        self.object.restaurant = self.get_restaurant()
        self.object.save()
        meal_formset.instance = self.object
        meal_formset.save()
        return HttpResponseRedirect(self.get_success_url())
        
    def get(self, request, *args, **kwargs):
        self.object = None
        form = MenuForm()
        meal_formset = MealFormset(request=request)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  meal_formset=meal_formset,))
                                  
    def get_context_data(self, **kwargs):
        context = super(MenuCreateView, self).get_context_data(**kwargs)
        context['restaurant'] = self.get_restaurant()
        return context
        
    def get_restaurant(self):
        pk = self.kwargs['restaurant_pk']
        return get_object_or_404(Restaurant, pk=pk)
                                  
    def get_success_url(self):
        return reverse('restaurant:restaurant_detail', kwargs={'pk': self.object.pk})
        
    def post(self, request, *args, **kwargs):
        self.object = None
        form = MenuForm(self.request.POST)
        meal_formset = MealFormset(self.request.POST, request=request)
        if (form.is_valid() and meal_formset.is_valid()):
            return self.form_valid(form, meal_formset)
        else:
            return self.form_invalid(form, meal_formset)
        
class MenuDetailView(DetailView):
    model = Restaurant
    