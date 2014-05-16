# -*- coding: utf-8 -*-
"""
Define your custom middlewares in this file.
"""
import base64
from django.contrib.auth import authenticate, login
from django.contrib.auth.middleware import RemoteUserMiddleware

__author__ = "flanker"


class DebugMiddleware(object):

    @staticmethod
    def process_request(request):
        request.META['HTTP_REMOTE_USER'] = 'flan'


class HttpBasicMiddleware(object):

    @staticmethod
    def process_request(request):
        if request.user.is_authenticated():
            return
        auth = request.META.get('HTTP_AUTHORIZATION')
        if auth:
            auth = auth.split()
            if len(auth) == 2 and auth[0].lower() == 'basic':
                username, password = base64.b64decode(auth[1]).decode('utf-8').split(':')
                user = authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    login(request, user)


class HttpRemoteUserMiddleware(RemoteUserMiddleware):
    header = 'HTTP_REMOTE_USER'
