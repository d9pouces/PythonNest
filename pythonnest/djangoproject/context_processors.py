# -*- coding: utf-8 -*-
"""
Define your custom context processors in this file.
"""
__author__ = "flanker"
# __copyright__ = "Copyright 2013, 19pouces.net"
# __credits__ = "flanker"
# __maintainer__ = "flanker"
# __email__ = "flanker@19pouces.net"


def context_user(request):
    """Add the current user to the context.
    User is taken from the current :class:`django.core.http.HttpRequest`
    and binded to `user`."""
    return {'user': request.user, }