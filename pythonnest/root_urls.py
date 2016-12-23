# -*- coding: utf-8 -*-

from django.conf.urls import url

from pythonnest import views
from pythonnest.views import xmlrpc


__author__ = 'Matthieu Gallet'

urls = [
    url(r'^index\.html$', views.index),
    url(r'^packages/(?P<order_by>(\-modification|normalized_name))\.html$', views.all_packages, name='all_packages'),
    url(r'^package/(?P<package_id>\d+)/(?P<release_id>\d+)\.html$', views.show_package, name='show_package'),
    url(r'^package/(?P<package_id>\d+)\.html$', views.show_package,
        name='show_package'),
    url(r'^pages/delete_role/(?P<role_id>\d+)\.html$', views.delete_role,
        name='delete_role'),
    url(r'^pages/delete_download/(?P<download_id>\d+)\.html$', views.delete_download, name='delete_download'),
    url(r'^pages/show_classifier/(?P<classifier_id>\d+)\.html$', views.show_classifier, name='show_classifier'),

    url(r'^pypi/(?P<package_name>[^/]+)/json$', views.package_json, name='package_json'),
    url(r'^pypi/(?P<package_name>[^/]+)/(?P<version>[^/]+)/json$', views.version_json, name='version_json'),
    url(r'^pypi/?$', xmlrpc, name='rpc4django'),
    url(r'^simple/(?P<package_name>[^/]+)/(?P<version>[^/]+)$', views.simple, name='simple'),
    url(r'^simple/(?P<package_name>[^/]+)/$', views.simple, name='simple'),
    url(r'^simple/$', views.simple, name='simple'),
    url(r'^setup/?$', views.setup, name='setup'),
]
