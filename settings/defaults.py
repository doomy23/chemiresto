# -*- coding: utf-8 -*-

import os.path
import sys
from getenv import env

##
## Paths
##
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'modules'))

##
## Debug
##
DEBUG = env('DJANGO_DEBUG')
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = (env('DJANGO_DEBUG_TOOLBAR_INTERNAL_IP'),)


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
## I18N & L18N
##
TIME_ZONE = 'America/Montreal'
LANGUAGES = (
  #('en', 'English'),
  ('fr', 'Français'),
)
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)


##
## Security
##
SECRET_KEY = 'QWERTY1234567890987654321!!!!!!!!'


##
## URL's
##
ROOT_URLCONF = 'urls'


##
## Deploy
##
WSGI_APPLICATION = 'wsgi.application'


##
## Domains
##
ALLOWED_HOSTS = ['*']


##
## Middlewares
##
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


##
## Media & Statics
##
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'base_static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


##
## Templates
##
TEMPLATE_LOADERS = (
    'django.template.loaders.eggs.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.debug',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)


##
## Apps
##
INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)


##
## Django Test Runner
##
TEST_RUNNER = 'django.test.runner.DiscoverRunner'


##
## Mail
##
EMAIL_USE_TLS = env('DJANGO_EMAIL_USE_TLS')
EMAIL_HOST = env('DJANGO_EMAIL_HOST'),
EMAIL_HOST_USER = env('DJANGO_EMAIL_HOST_USER'),
EMAIL_HOST_PASSWORD = env('DJANGO_EMAIL_HOST_PASSWORD'),
EMAIL_PORT = env('DJANGO_EMAIL_PORT')


##
## Admins
##
ADMINS = (
        ('Dominic Roberge', 'doomy23@gmail.com'),
		('Etienne Caya', 'etiennecaya@gmail.com'),
)
MANAGERS = ADMINS


##
## Logs
##
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

