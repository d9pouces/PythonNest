# -*- coding: utf-8 -*-
"""
Define a main() function, allowing you to manage your Django project.
"""
import os
import sys
__author__ = "flanker"
# __copyright__ = "Copyright 2013, 19pouces.net"
# __credits__ = "flanker"
# __maintainer__ = "flanker"
# __email__ = "flanker@19pouces.net"

def main():
    """
    Main function, calling Django code for management commands.
    """
    os.environ["DJANGO_SETTINGS_MODULE"] = "pythonnest.djangoproject.settings"
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)