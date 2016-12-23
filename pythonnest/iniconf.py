# -*- coding: utf-8 -*-
from djangofloor.conf.mapping import INI_MAPPING as DEFAULTS
__author__ = 'flanker'


INI_MAPPING = [x for x in DEFAULTS if x.name.partition('.')[0] in ('global', 'database', 'email')]
