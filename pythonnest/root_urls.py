# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rpc4django.views import serve_rpc_request
from pythonnest import views
from ajax_select import urls as ajax_select_urls

__author__ = 'Matthieu Gallet'

urls = [
    url('^index\.html$', views.index),
    url(r'^index-(?P<page>\d+)\.html$', views.index),
    url(r'^pages/show_package/(?P<package_id>\d+)/(?P<release_id>\d+)\.html$', views.show_package),
    url(r'^pages/show_package/(?P<package_id>\d+)\.html$', views.show_package),
    url(r'^pages/delete_role/(?P<role_id>\d+)\.html$', views.delete_role),
    url(r'^pages/delete_download/(?P<download_id>\d+)\.html$', views.delete_download),
    url(r'^pages/show_classifier/(?P<classifier_id>\d+)\.html$', views.show_classifier),
    url(r'^pages/show_classifier/(?P<classifier_id>\d+)/(?P<page>\d+)\.html$', views.show_classifier),

    url(r'^pypi/(?P<package_name>[^/]+)/json$', views.package_json),
    url(r'^pypi/(?P<package_name>[^/]+)/(?P<version>[^/]+)/json$', views.version_json),
    url(r'^pypi/?$', serve_rpc_request),
    url(r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^simple/(?P<package_name>[^/]+)/(?P<version>[^/]+)$', views.simple),
    url(r'^simple/(?P<package_name>[^/]+)/$', views.simple),
    url(r'^simple/$', views.simple),
    url(r'^setup/?$', views.setup),

]
