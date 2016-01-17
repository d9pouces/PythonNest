# -*- coding: utf-8 -*-
__author__ = 'flanker'
from djangofloor.iniconf import OptionParser, bool_setting, INI_MAPPING as DEFAULTS


def x_accel_converter(value):
    if bool_setting(value):
        return [('{MEDIA_ROOT}', '{MEDIA_URL}'), ]
    return []


INI_MAPPING = [x for x in DEFAULTS if x.setting_name not in ('FLOOR_DEFAULT_GROUP_NAME', 'FLOOR_AUTHENTICATION_HEADER')]
INI_MAPPING += [OptionParser('BIND_ADDRESS', 'global.bind_address', doc_default_value='localhost:8130'), ]