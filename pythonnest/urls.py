# -*- coding: utf-8 -*-
"""Define mappings from the URL requested by a user to a proper Python view."""
from django.conf.urls import patterns, url
__author__ = "flanker"
# __copyright__ = "Copyright 2013, 19pouces.net"
# __credits__ = "flanker"
# __maintainer__ = "flanker"
# __email__ = "flanker@19pouces.net"

urlpatterns = patterns(  # pylint: disable=C0103
    '',
    url(r'^index/$', 'pythonnest.views.index'),
)