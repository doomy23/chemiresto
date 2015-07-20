# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'^create/$', RestaurantCreateView.as_view(), name="restaurant_create"),
    url(r'^(?P<pk>\d+)/$', RestaurantDetailView.as_view(), name="restaurant_detail"),
    url(r'^(?P<pk>\d+)/delete/$', RestaurantDeleteView.as_view(), name="restaurant_delete"),
    url(r'^$', RestaurantsView.as_view(), name="restaurants"),
    url(r'^list/$', RestaurantListView.as_view(), name="restaurant_list"),
    
    url(r'^(?P<restaurant_pk>\d+)/menus/create/$', MenuCreateView.as_view(), name="menu_create"),
    url(r'^(?P<restaurant_pk>\d+)/menus/(?P<pk>\d+)/$', MenuDetailView.as_view(), name="menu_detail"),
)
