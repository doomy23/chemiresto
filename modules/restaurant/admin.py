# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Restaurant, Menu, Meal

class RestaurantAdmin(admin.ModelAdmin):
    pass

class MenuAdmin(admin.ModelAdmin):
    pass

class MealAdmin(admin.ModelAdmin):
    pass

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Meal, MealAdmin)
