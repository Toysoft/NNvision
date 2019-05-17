"""
Django settings for djangoticia project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i5dbw16+)@q7s-lgi#+do!j8f)u2#qvy1inhu&ib&#s%)ko%-t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'app1.apps.App1Config',
    'app2.apps.App2Config',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'projet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'database', 'db.sqlite3'),
        'OPTIONS': {
            'timeout': 10,  # in seconds
            # see also
            # https://docs.python.org/3.7/library/sqlite3.html#sqlite3.connect
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

# Provide a lists of languages which your site supports.
LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../static_root')

# URL that your MEDIA files will be accessible through the browser.
MEDIA_URL = '/media/'
# Physical system path where the static files are stored. Files that are being uploaded by the user.
MEDIA_ROOT = os.path.join(BASE_DIR, '../media_root')

LOGOUT_REDIRECT_URL = '/'

CFG = 'cfg/yolov3-spp.cfg'
WEIGHTS = '../weights/yolov3-spp.weights'
DATA = 'cfg/coco.data'
PYTHON = 'python3'

EMAIL_HOST = 'ssl0.ovh.net'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'contact@protecia.com'
EMAIL_HOST_PASSWORD = '25011975*jJ'
EMAIL_USE_SSL = True

# Your Account SID from twilio.com/console
ACCOUNT_SID = "AC445238ce002d1c440c77883963183c04"
# Your Auth Token from twilio.com/console
AUTH_TOKEN  = "97c36acf2c85e62436181e878305f982"

VERSION='1.0.2'
DARKNET_PATH='/NNvision/darknet_alex_201903'
THREATED_REQUESTS=True
PUBLIC_SITE='http://'
ACCESS_NO_FREE = True
ACCESS_ADAM = True
ACCESS_HOOK = True
WAIT_BEFORE_DETECTION = 20
DATASET_TEST = False

RESELLER_LOGO = 'logo-telegil.png'
 
