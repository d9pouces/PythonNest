# -*- coding: utf-8 -*-
from djangofloor.conf.fields import BooleanConfigField
from djangofloor.conf.mapping import BASE_MAPPING, REDIS_MAPPING
__author__ = 'flanker'

VALUES = [

    BooleanConfigField('global.read_only', 'READ_ONLY_MIRROR', 'Set to "true" if this mirror is a read-only mirror.'
                                                               'No update can be made by users.'),
]
INI_MAPPING = BASE_MAPPING + REDIS_MAPPING + VALUES
