# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

import accounts
import restaurants

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls), name="admin"),
	url(r'^accounts/', include(accounts.urls, namespace="accounts")),
    url(r'^restaurants/', include(restaurants.urls, namespace="restaurants")),
	url(r'^$', restaurants.views.RestaurantsView.as_view(), name="home")
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
