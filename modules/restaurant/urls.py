# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'^list/$', RestaurantListView.as_view(), name="restaurant_list"),
)
