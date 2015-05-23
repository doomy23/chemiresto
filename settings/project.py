# -*- coding: utf-8 -*-

from defaults import *
from getenv import env

INSTALLED_APPS += (
    # 3rd parties
    "crispy_forms",
    "django_countries",
    
    # Modules
    "accounts",
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'