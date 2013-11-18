# -*- coding: utf-8 -*-
""" Django settings for pythonnest project. """
import configparser
from os.path import join, dirname, abspath
from urllib.parse import urlparse

__author__ = "flanker"


__parser = configparser.ConfigParser()
__config_path_comp = abspath(__file__).split('/')
__config_files = [join(__file__, '..', '..', 'pythonnest.ini')]
if 'lib' in __config_path_comp:
    __config_files.append('/'.join(__config_path_comp[0:__config_path_comp.index('lib')] + ['etc', 'pythonnest.ini']))
__parser.read(__config_files)

ROOT_PATH = __parser.get('pythonnest', 'ROOT_PATH', fallback=None)
if not ROOT_PATH:
    ROOT_PATH = abspath(join(dirname(dirname(dirname(__file__))), 'django_data'))
HOST = __parser.get('pythonnest', 'HOST', fallback='http://localhost:8000/')
DEBUG = __parser.getboolean('pythonnest', 'DEBUG', fallback=True)
TIME_ZONE = __parser.get('pythonnest', 'TIME_ZONE', fallback='Europe/Paris')
LANGUAGE_CODE = __parser.get('pythonnest', 'LANGUAGE_CODE', fallback='fr-fr')
USE_XSENDFILE = __parser.getboolean('pythonnest', 'USE_XSENDFILE', fallback=False)
DATABASE_ENGINE = __parser.get('pythonnest', 'DATABASE_ENGINE', fallback='django.db.backends.sqlite3')
DATABASE_NAME = __parser.get('pythonnest', 'DATABASE_NAME', fallback=None)
if not DATABASE_NAME:
    DATABASE_NAME = join(ROOT_PATH, 'database.sqlite3')
DATABASE_USER = __parser.get('pythonnest', 'DATABASE_USER', fallback='')
DATABASE_PASSWORD = __parser.get('pythonnest', 'DATABASE_PASSWORD', fallback='')
DATABASE_HOST = __parser.get('pythonnest', 'DATABASE_HOST', fallback='')
DATABASE_PORT = __parser.get('pythonnest', 'DATABASE_PORT', fallback='')

ADMIN_EMAIL = __parser.get('pythonnest', 'ADMIN_EMAIL', fallback='admin@example.com')

ADMINS = ((ADMIN_EMAIL, ADMIN_EMAIL), )

__components = urlparse(HOST)
TEMPLATE_DEBUG = DEBUG
MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [__components.hostname]


DATABASES = {
    'default': {
        'ENGINE': DATABASE_ENGINE,  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DATABASE_NAME,   # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': DATABASE_PORT,  # Set to empty string for default.
    }
}

SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = join(ROOT_PATH, 'media')
MEDIA_URL = HOST + 'media/'
STATIC_ROOT = join(ROOT_PATH, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = ()

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4f4&@pcm_@017&l27o1#4pch-@g15&d@2rs3jccrxr@zd0h1@7'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pythonnest.djangoproject.middleware.HttpBasicMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.RemoteUserBackend',
                           'django.contrib.auth.backends.ModelBackend', ]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'pythonnest.djangoproject.context_processors.context_user',
)


ROOT_URLCONF = 'pythonnest.djangoproject.root_urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'pythonnest.djangoproject.wsgi.application'

TEMPLATE_DIRS = (
    abspath(join(dirname(__file__), 'templates')),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'rpc4django',
    'pythonnest',
    'pythonnest.rpcapi',
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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