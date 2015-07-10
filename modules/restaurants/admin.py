# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Restaurant, Meal, MealTag

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'address1', 'address2')
    
    #def get_queryset(self, request):
    #    qs = super(RestaurantAdmin, self).get_queryset(request)
    #    return qs.filter(user=request.user).order_by('name')

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant')
    
@admin.register(MealTag)
class MealAdmin(admin.ModelAdmin):
    list_display = ('tag', 'repas')
    
    def repas(self, obj):
        return obj.meals.all().count()
    