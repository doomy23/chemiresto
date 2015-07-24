# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib import admin

import views

urlpatterns = patterns('',
	url(r'^$', views.HomeView.as_view(), name="home"),
	url(r'^admin/', include(admin.site.urls)), # Utile dans quelques rare cas
	url(r'^accounts/', include(accounts.urls, namespace="accounts")),
    url(r'^restaurant/', include(restaurant.urls, namespace="restaurant")),
    url(r'^select_language/(?P<lang_code>\w+)/$', views.SelectLanguageView.as_view(), name="select_language"),
    url(r'^about/', views.TemplateView.as_view(template_name="about.html"), name="about"),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
