# -*- coding: utf-8 -*-
"""
Django settings for pizzafria project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.abspath(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret secretkey.txt used in production secret!
with open(os.path.join(BASE_DIR, 'secretkey.txt')) as f:
    SECRET_KEY = f.read().strip()
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'podcast',
    'licenses',
    'easy_thumbnails',
    'podcasting',
    'imagekit',
    'sorl.thumbnail',
    'blog',
    'tinymce'
)
TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'height': 500,
    'relative_urls': False
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'pizzafria.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_PATH, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'blog.context_processor.latest_entries'
            ],
        },
    },
]

WSGI_APPLICATION = 'pizzafria.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# DATABASES readed from database.json containing the complete configuration
# The file contains the folowing json
#{
#    "default": {
#        "ENGINE": "django.db.backends.mysql",
#        "NAME": "podcast_db",
#        "USER": "podcast_dbuser",
#        "PASSWORD": "dbpass",
#        "HOST": "localhost",
#        "PORT": "3306"
#    }
#}
with open(PROJECT_PATH + '/database.json') as f:
    db = [line.rstrip('\n') for line in f]
    db = ''.join(db)

DATABASES = json.loads(db)

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_PATH, 'templates/static/')

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'templates/media/')

SITE_URL = 'pizzafria.com'
SITE_ID = 1

THUMBNAIL_ALIASES = {
    "podcasting.Show.original_image": {
        "sm": {"size": (120, 120)},
        "lg": {"size": (550, 550)},
        "itunes_sm": {"size": (144, 144)},
        "itunes_lg": {"size": (1400, 1400)},
    },
    "podcasting.Episode.original_image": {
        "sm": {"size": (120, 120)},
        "lg": {"size": (550, 550)},
        "itunes_sm": {"size": (144, 144)},
        "itunes_lg": {"size": (1400, 1400)},
    },
}
PODCASTING_FEED_ENTRIES = 100
ITUNES_URL = "https://itunes.apple.com/mx/podcast/pizza-fria/id1024808184?l=en"
PODCAST_DOMAIN = 'http://pizzafria.com'
# If you're not using a podtrack, please use just the protocol as the tracking prephix
# TRACKING_PREPHIX = 'http://'
TRACKING_PREPHIX = 'http://dts.podtrac.com/redirect.mp3/'
