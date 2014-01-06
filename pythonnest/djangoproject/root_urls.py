# -*- coding: utf-8 -*-
"""Define mappings from the URL requested by a user to a proper Python view."""
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from ajax_select import urls as ajax_select_urls
from urllib.parse import urlparse

__author__ = "flanker"
admin.autodiscover()

MEDIA_PATH = urlparse(settings.MEDIA_URL).path[1:]

urlpatterns = patterns('',
                       #    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
                       (r'^logcreate/$', 'pythonnest.views.create_user', {'template_name': 'create_user.html'}),
                       (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
                       (r'^logchange/$', 'django.contrib.auth.views.password_change',
                        {'template_name': 'password_change.html', 'post_change_redirect': '/'}),
                       url(r'^admin/', include(admin.site.urls)),
                       (r'^jsi18n/$', 'django.views.i18n.javascript_catalog',
                        {'packages': ('pythonnest', 'django.contrib.admin', ), }),
                       (r'^' + settings.MEDIA_URL[1:] + '(?P<path>.*)$', 'pythonnest.views.static_serve',
                        {'document_root': settings.MEDIA_ROOT}),
                       (r'^' + settings.STATIC_URL[1:] + '(?P<path>.*)$', 'pythonnest.views.static_serve',
                        {'document_root': settings.STATIC_ROOT}),
                       url(r'^pypi/(?P<package_name>[^/]+)/json$', 'pythonnest.views.package_json'),
                       url(r'^pypi/(?P<package_name>[^/]+)/(?P<version>[^/]+)/json$', 'pythonnest.views.version_json'),
                       url(r'^pypi/?$', 'rpc4django.views.serve_rpc_request'),
                       url(r'^pythonnest/', include('pythonnest.urls')),
                       (r'^admin/lookups/', include(ajax_select_urls)),
                       url(r'^simple/(?P<package_name>[^/]+)/(?P<version>[^/]+)$', 'pythonnest.views.simple'),
                       url(r'^simple/(?P<package_name>[^/]+)/$', 'pythonnest.views.simple'),
                       url(r'^simple/$', 'pythonnest.views.simple'),
                       url(r'^setup/?$', 'pythonnest.views.setup'),
                       url(r'^$', 'pythonnest.views.index'), )
