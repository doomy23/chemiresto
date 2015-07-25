# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^create/$', views.OrderCreatorView.as_view(), name="create"),
    url(r'^view/(?P<id>.+)/$', views.OrderDetailView.as_view(), name="detail"),
)
