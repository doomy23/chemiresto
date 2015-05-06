# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', TemplateView.as_view(template_name="index.html"), name="home")
)

if settings.DEBUG:
	urlpatterns += static(r'^media/', document_root=settings.MEDIA_ROOT)
	urlpatterns += static(r'^static/', document_root=settings.STATIC_ROOT)
