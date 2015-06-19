# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from views import *
from restaurator_views import *

urlpatterns = patterns('',
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^manage/$', ManagerView.as_view(), name="manage_account"),
    url(r'^delete/(?P<pk>\d+)/$', DeleteUserView.as_view(), name="delete_account"),
    
    url(r'^restaurators/create/$', CreateRestauratorView.as_view(), name="restaurators_create"),
    url(r'^restaurators/$', RestauratorDashView.as_view(), name="restaurators_dash"),
)
