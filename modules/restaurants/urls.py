# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'^create/$', RestaurantCreateView.as_view(), name="restaurant_create"),
    url(r'^(?P<id>.+)/$', RestaurantsDetailsView.as_view(), name="restaurants_details"),
    url(r'^$', RestaurantsView.as_view(), name="restaurants_list")
)
