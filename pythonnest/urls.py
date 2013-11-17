# -*- coding: utf-8 -*-
"""Define mappings from the URL requested by a user to a proper Python view."""
from django.conf.urls import patterns, url
__author__ = "flanker"

urlpatterns = patterns(  # pylint: disable=C0103
    '',
    url(r'^index/$', 'pythonnest.views.index'),
    url(r'^index/(?P<page>\d+)/$', 'pythonnest.views.index'),
    url(r'^show_package/(?P<package_id>\d+)/(?P<release_id>\d+)/$', 'pythonnest.views.show_package'),
    url(r'^show_package/(?P<package_id>\d+)/$', 'pythonnest.views.show_package'),
    url(r'^show_classifier/(?P<classifier_id>\d+)/$', 'pythonnest.views.show_classifier'),
    url(r'^show_classifier/(?P<classifier_id>\d+)/(?P<page>\d+)/$', 'pythonnest.views.show_classifier'),
)