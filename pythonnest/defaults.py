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
USE_CELERY = False

FLOOR_INDEX = 'pythonnest.views.index'
LISTEN_ADDRESS = 'localhost:8130'
FLOOR_TEMPLATE_CONTEXT_PROCESSORS = ['pythonnest.context_processors.context_user', ]
