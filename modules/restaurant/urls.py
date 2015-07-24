# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
    # Pour l'entrepreneur
    url(r'^create/$', RestaurantCreateView.as_view(), name="restaurant_create"),
    url(r'^(?P<pk>\d+)/update/$', RestaurantUpdateView.as_view(), name="restaurant_update"),
    url(r'^(?P<pk>\d+)/delete/$', RestaurantDeleteView.as_view(), name="restaurant_delete"),
    url(r'^list/$', RestaurantListView.as_view(), name="restaurant_list"),
    
    # Pour les restaurateurs
    url(r'^(?P<restaurant_pk>\d+)/menus/create/$', MenuCreateView.as_view(), name="menu_create"),
    url(r'^menus/list/$', MenuListView.as_view(), name="menu_list"),
    
    # Public
    url(r'^(?P<pk>\d+)/$', RestaurantDetailView.as_view(), name="restaurant_detail"),
    url(r'^$', RestaurantsView.as_view(), name="restaurants"),
)
