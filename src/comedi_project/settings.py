"""
Django settings for comedi_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
from django.utils.translation import gettext_lazy as _

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '19ql0m@@y8fc4=_i4_no^0f#d@6$*!@t3=ifst&5-c%ytyl5p!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'comedi',
    'picklefield',
#     'django.contrib.sites',
#     'django_options',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',


    'constance.backends.database',
    'constance',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'django_options.middleware.OptionsLoaderMiddleware',
    'django.middleware.locale.LocaleMiddleware',

)

ROOT_URLCONF = 'comedi_project.urls'

WSGI_APPLICATION = 'comedi_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


#DATABASES = {
#    'default': {
#        'ENGINE':'django.db.backends.mysql',
#        'NAME': 'comedi',
#        'USER': 'comedi_user',
#        'PASSWORD': 'password',
#        'HOST': '/var/run/mysqld/mysqld.sock',
#        'PORT': '3306',
#    }
#}
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
LANGUAGES = ( 
    ( 'fr', _( 'Francais' ) ),
#     ( 'en', _( 'Anglais' ) ),

 )

LOCALE_PATHS = ( 
    'locale/',
 )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = '/login/'
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
SITE_ID = 2

TEMPLATE_CONTEXT_PROCESSORS = ( 
    # ...
    'django.contrib.auth.context_processors.auth',
    'constance.context_processors.config',
    "django.core.context_processors.i18n",
 )


from datetime import datetime

CONSTANCE_CONFIG = {
    'PHONE_START': ( '', 'Prefix par defaut du telephone' ),
    'LOCK_ORDER_ORIGIN' : ( False, "Bloquer l'origine de la commande" ),
#     'OWNER': ( 'Mr. Henry Wensleydale', 'owner of the shop' ),
#     'MUSICIANS': ( 4, 'number of musicians inside the shop' ),
#     'DATE_ESTABLISHED': ( datetime( 1972, 11, 30 ), "the shop's first opening" ),
}

# DATE_INPUT_FORMATS = (
#     '%Y-%m-%d', '%d-%m-%Y', '%m/%d/%y',  # '2006-10-25', '10/25/2006', '10/25/06'
#  )

