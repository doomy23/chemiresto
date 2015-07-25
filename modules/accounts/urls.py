# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
import views
import restaurateur_views

urlpatterns = patterns('',
    url(r'^register/$', views.RegisterView.as_view(), name="register"),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
    
    url(r'^manage/$', views.ManagerView.as_view(), name="manage_account"),
    url(r'^dashboard/$', views.DashboardView.as_view(), name="dashboard"),
    url(r'^delete/(?P<pk>\d+)/$', views.DeleteUserView.as_view(), name="delete_account"),
    
    url(r'^restaurateurs/create/$', restaurateur_views.CreateRestaurateurView.as_view(), name="restaurateurs_create"),
    url(r'^restaurateurs/(?P<pk>\d+)/manage/$', restaurateur_views.ManageRestaurateurView.as_view(), name="restaurateurs_manage"),
    url(r'^restaurateurs/(?P<pk>\d+)/delete/$', restaurateur_views.DeleteRestaurateurView.as_view(), name="restaurateurs_delete"),
    url(r'^restaurateurs/list/$', restaurateur_views.RestaurateurListView.as_view(), name="restaurateurs_list"),
)
