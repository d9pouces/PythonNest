#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from djangofloor.scripts import gunicorn
os.environ['DF_CONF_NAME'] = 'pythonnest-gunicorn'
gunicorn()
