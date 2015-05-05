# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls))
)

if settings.DEBUG:
	urlpatterns += static(r'^media/', document_root=settings.MEDIA_ROOT)
	urlpatterns += static(r'^static/', document_root=settings.STATIC_ROOT)
