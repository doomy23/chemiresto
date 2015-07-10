# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'^list/$', RestaurantsView.as_view(), name="restaurants_list"),
    url(r'^(?P<id>.+)/$', RestaurantsDetailsView.as_view(), name="restaurants_details")
)
