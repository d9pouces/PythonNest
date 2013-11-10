# -*- coding: utf-8 -*-
"""
Print basic but functionnal configurations for deployment.
"""
import logging
import os.path
from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
__author__ = "flanker"


class Command(BaseCommand):
    """Print basic configuration files for different kinds of deployment"""
    # pylint: disable=R0912
    # pylint: disable=R0915
    args = ''
    help = 'Print basic configuration files for different kinds of deployment'

    def handle(self, *args, **options):
        # first: determine the type of server
        server_type = None
        server_name = input('domain name of your server [www.example.com] ')
        if not server_name:
            server_name = 'www.example.com'
        use_ssl = None
        while use_ssl is None:
            use_ssl = input('Secure connection by SSL y/n [y] ')
            if not use_ssl:
                use_ssl = 'y'
            if use_ssl not in ('y', 'n'):
                print('Please enter y or n.')
                use_ssl = None
        while server_type is None:
            print('Which server do you want to use?')
            server_type = input('1: Apache, 2: Nginx [1] ')
            if not server_type:
                server_type = '1'
            if server_type not in ('1', '2'):
                print('Please enter 1 or 2.')
                server_type = None
        context = {'main_port': 443 if use_ssl == 'y' else 80,
                   'server_name': server_name,
                   'static_root': settings.STATIC_ROOT,
                   'static_url': settings.STATIC_URL,
                   'media_url': settings.MEDIA_URL,
                   'media_root': settings.MEDIA_ROOT,
                   'use_ssl': use_ssl == 'y',
                   'alt_port': 80 if use_ssl == 'y' else None,
                   }
        if server_name not in settings.ALLOWED_HOSTS:
            msg = 'You must add "%s" to your settings.ALLOWED_HOSTS' % server_name
            logging.warning(msg)
        print('Which method do you want to use?')
        daemon_type = None
        if server_type == '1':
            template = 'deployment/apache.conf'
            while daemon_type is None:
                daemon_type = input('1: mod_wsgi, 2: gunicorn ')
                if daemon_type not in ('1', '2'):
                    print('Please enter 1 or 2.')
                    daemon_type = None
            if daemon_type == '1':
                from pythonnest.djangoproject import wsgi
                import pythonnest
                context['wsgi_path'] = wsgi.__file__
                context['python_path'] = os.path.dirname(os.path.dirname(pythonnest.__file__))
#                   'virtual_env': virtual_env,
            else:
                print('Default port for gunicorn is 8000')
                context['gunicorn_port'] = 8000
                if 'gunicorn' not in settings.INSTALLED_APPS:
                    logging.warning('You must add "gunicorn" to your settings.INSTALLED_APPS')
        else:
            template = 'deployment/nginx.conf'
            while daemon_type is None:
                daemon_type = input('1: fast_cgi, 2: gunicorn ')
                if daemon_type not in ('1', '2'):
                    print('Please enter 1 or 2.')
                    daemon_type = None
            if daemon_type == '1':
                try:
                    #noinspection PyPackageRequirements,PyUnresolvedReferences
                    import flup
                    msg = 'Found flup at %s' % os.path.dirname(flup.__file__)
                    logging.debug(msg)
                except ImportError:
                    logging.warning('You must install "flup"')
                context['fcgi_port'] = 3033
                print('Default port for fast cgi is %d' % context['fcgi_port'])
                print('Use manage.py runfcgi method=threaded host=127.0.0.1 port=%d' % context['fcgi_port'])
            else:
                context['gunicorn_port'] = 8000
                print('Default port for gunicorn is %d' % context['gunicorn_port'])
                try:
                    #noinspection PyPackageRequirements,PyUnresolvedReferences
                    import gunicorn
                    msg = 'Found gunicorn at %s' % os.path.dirname(gunicorn.__file__)
                    logging.debug(msg)
                except ImportError:
                    logging.warning('You must install "gunicorn"')
                if 'gunicorn' not in settings.INSTALLED_APPS:
                    logging.warning('You must add "gunicorn" to your settings.INSTALLED_APPS')
        print(render_to_string(template, context))