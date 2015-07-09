# -*- coding: utf-8 -*-
from django.views.generic.list import ListView

from models import Restaurant

class RestaurantListView(ListView):
    model = Restaurant
    context_object_name = "restaurants"
    template_name = 'restaurants/list.html'
    
    def get_queryset(self):
        request = self.request
        city = request.GET.get('c')
        
        if city:
            return Restaurant.objects.filter(city=city).order_by('name')
        else:
            if request.user and request.user_details:
                return Restaurant.objects.filter(city=request.user_details.city).order_by('name')
            else: 
                return Restaurant.objects.all().order_by('name')
