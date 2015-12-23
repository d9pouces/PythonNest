# -*- coding: utf-8 -*-
__author__ = 'Matthieu Gallet'


########################################################################################################################
# sessions
########################################################################################################################
SESSION_REDIS_PREFIX = 'session'
SESSION_REDIS_HOST = '{REDIS_HOST}'
SESSION_REDIS_PORT = '{REDIS_PORT}'
SESSION_REDIS_DB = 10
READ_ONLY = False

########################################################################################################################
# caching
########################################################################################################################
# CACHES = {
#     'default': {'BACKEND': 'django_redis.cache.RedisCache', 'LOCATION': 'redis://{REDIS_HOST}:{REDIS_PORT}/11',
#      'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#      'PARSER_CLASS': 'redis.connection.HiredisParser', }, },
#     }

########################################################################################################################
# django-redis-websocket
########################################################################################################################

########################################################################################################################
# celery
########################################################################################################################

FLOOR_INSTALLED_APPS = ['pythonnest', 'rpc4django', ]
FLOOR_INDEX = 'pythonnest.views.index'
FLOOR_URL_CONF = 'pythonnest.root_urls.urls'
FLOOR_PROJECT_NAME = 'PythonNest'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ap6WerC2w8c6SGCPvFM5YDHdTXvBnzHcToS0J3r6LeetzReng6'





if __name__ == '__main__':
    import doctest
    doctest.testmod()
