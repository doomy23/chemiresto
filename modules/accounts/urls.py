# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
import views
import restaurator_views

urlpatterns = patterns('',
    url(r'^register/$', views.RegisterView.as_view(), name="register"),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
    
    url(r'^manage/$', views.ManagerView.as_view(), name="manage_account"),
    url(r'^dashboard/$', views.DashboardView.as_view(), name="dashboard"),
    url(r'^delete/(?P<pk>\d+)/$', views.DeleteUserView.as_view(), name="delete_account"),
    
    url(r'^restaurators/create/$', restaurator_views.CreateRestauratorView.as_view(), name="restaurators_create"),
    url(r'^restaurators/(?P<pk>\d+)/manage/$', restaurator_views.ManageRestauratorView.as_view(), name="restaurators_manage"),
    url(r'^restaurators/(?P<pk>\d+)/delete/$', restaurator_views.DeleteRestauratorView.as_view(), name="restaurators_delete"),
    url(r'^restaurators/list/$', restaurator_views.RestauratorListView.as_view(), name="restaurators_list"),
)
