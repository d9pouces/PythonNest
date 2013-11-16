# -*- coding: utf-8 -*-
"""Define mappings from the URL requested by a user to a proper Python view."""
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
__author__ = "flanker"
admin.autodiscover()

from urllib.parse import urlparse

MEDIA_PATH = urlparse(settings.MEDIA_URL).path[1:]

urlpatterns = patterns(  # pylint: disable=C0103
    '',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)), 
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': ('pythonnest', 'django.contrib.admin', ), }),
    (r'^' + settings.MEDIA_URL[1:] + '(?P<path>.*)$', 'pythonnest.views.static_serve',
     {'document_root': settings.MEDIA_ROOT}),
    (r'^' + settings.STATIC_URL[1:] + '(?P<path>.*)$', 'pythonnest.views.static_serve',
     {'document_root': settings.STATIC_ROOT}),
    url(r'^pypi/(?P<package_name>[^/]+)/json$', 'pythonnest.views.package_json'),
    url(r'^pypi/(?P<package_name>[^/]+)/(?P<version>[^/]+)/json$', 'pythonnest.views.version_json'),
    url(r'^pypi/?$', 'rpc4django.views.serve_rpc_request'),
    url(r'^pythonnest/', include('pythonnest.urls')),
    url(r'^simple/(?P<package_name>[^/]+)/(?P<version>[^/]+)$', 'pythonnest.views.simple'),
    url(r'^simple/(?P<package_name>[^/]+)/$', 'pythonnest.views.simple'),
    url(r'^simple/$', 'pythonnest.views.simple'),
    url(r'^setup/?$', 'pythonnest.views.setup'),
    url(r'^$', 'pythonnest.views.index'),
)
