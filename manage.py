#!/usr/bin/env python
from djangofloor.scripts import manage
import os
os.environ['DJANGOFLOOR_PROJECT_NAME'] = 'pythonnest'
manage()