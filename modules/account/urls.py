# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'^register/$', RegisterView.as_view(), name="Register"),
    url(r'^login/$', LoginView.as_view(), name="Login")
)