# -*- coding: utf-8 -*-
__author__ = 'Matthieu Gallet'


########################################################################################################################
# caching
########################################################################################################################
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', 'LOCATION': 'unique-snowflake'}}
WEBSOCKET_URL = None
DF_INDEX_VIEW = 'pythonnest.views.index'
DF_INSTALLED_APPS = ['pythonnest', ]
DF_URL_CONF = 'pythonnest.root_urls.urls'
READ_ONLY_MIRROR = True
# DF_TEMPLATE_CONTEXT_PROCESSORS = ['pythonnest.context_processors.context_user', ]
USE_CELERY = False

FLOOR_INDEX = 'pythonnest.views.index'
# FLOOR_URL_CONF = 'pythonnest.root_urls.urls'
# FLOOR_PROJECT_NAME = 'PythonNest'
# LISTEN_ADDRESS = 'localhost:8130'
# Make this unique, and don't share it with anybody.
# SECRET_KEY = 'ap6WerC2w8c6SGCPvFM5YDHdTXvBnzHcToS0J3r6LeetzReng6'
# READ_ONLY_MIRROR_HELP = 'Allow people to create and upload packages'
FLOOR_TEMPLATE_CONTEXT_PROCESSORS = ['pythonnest.context_processors.context_user', ]
MIDDLEWARE_CLASSES = ['django.middleware.cache.UpdateCacheMiddleware',
                      'django.middleware.common.CommonMiddleware',
                      # 'debug_toolbar.middleware.DebugToolbarMiddleware',
                      'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.locale.LocaleMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware',
                      'django.middleware.security.SecurityMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware',
                      'django.middleware.clickjacking.XFrameOptionsMiddleware',
                      'djangofloor.middleware.IEMiddleware',
                      'django.middleware.cache.FetchFromCacheMiddleware', ]
LANGUAGE_CODE = 'fr-FR'
