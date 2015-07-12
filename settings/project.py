# -*- coding: utf-8 -*-

from defaults import *
from getenv import env

##
## Admins
##
ADMINS = (
    (u'Dominic Roberge', 'doomy23@gmail.com'),
    (u'Anthony Martin Coallier', 'anthonymartincoallier.3@gmail.com'),
    (u'André Koolen', 'andre_koolen@hotmail.com'),
)

MANAGERS = ADMINS

##
## Database
##
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': env('SQLITE_DB')
    }
}

##
## Modules and Project's 3rd parties
##

# Has to be on top:
INSTALLED_APPS = (
    "suit",
) + INSTALLED_APPS

INSTALLED_APPS += (
    # 3rd parties
    "crispy_forms",
    "django_countries",
    
    # Modules
    "extras",
    "accounts",
    "restaurants",
    "orders",
)

MIDDLEWARE_CLASSES += (
    'accounts.middlewares.AccountTypeMiddleware',
)

##
## Paypal
##
PAYPAL_SANDBOX = env('PAYPAL_SANDBOX')
PAYPAL_SANDBOX_API = env('PAYPAL_SANDBOX_API')
PAYPAL_SANDBOX_CLIENT = env('PAYPAL_SANDBOX_CLIENT')
PAYPAL_SANDBOX_SECRET = env('PAYPAL_SANDBOX_SECRET')
PAYPAY_API = env('PAYPAY_API')
PAYPAL_CLIENT = env('PAYPAL_CLIENT')
PAYPAL_SECRET = env('PAYPAL_SECRET')

##
## Other stuff
##
CRISPY_TEMPLATE_PACK = 'bootstrap3'
