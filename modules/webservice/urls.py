# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^test/$', views.test, name="test"),
    url(r'^accounts/update/my_account/$', views.update_my_accounts, name="my_accounts"),
)
