# -*- coding: utf-8 -*-

from django.views.generic.list import ListView
from models import Restaurant

class RestaurantListView(ListView):
    model = Restaurant
    context_object_name = "restaurants"
    template_name = 'restaurant/list.html'
    
    def get_queryset(self):
        return Restaurant.objects.all().order_by('name')
