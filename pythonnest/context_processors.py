# -*- coding: utf-8 -*-
from django.conf import settings

__author__ = 'Matthieu Gallet'


# noinspection PyUnusedLocal
def context_user(request):
    """Add values specific to PythonNest."""
    return {'read_only_mirror': settings.READ_ONLY_MIRROR, }
