# -*- coding: utf-8 -*-
from django.conf import settings
from pythonnest import __version__ as version, __author__ as author
__author__ = 'Matthieu Gallet'


# noinspection PyUnusedLocal
def context_user(request):
    """Add values specific to PythonNest."""
    return {'read_only_mirror': settings.READ_ONLY_MIRROR, 'version': version, 'author': author}
