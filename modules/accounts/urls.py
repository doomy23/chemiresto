# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^manage/$', ManagerView.as_view(), name="manage_account"),
    url(r'^delete/(?P<pk>\d+)/$', DeleteUserView.as_view(), name="delete_account"),
)
