# -*- coding: utf-8 -*-
"""
Define a main() function, allowing you to manage your Django project.
"""
import os
import sys
__author__ = "flanker"


def main():
    """
    Main function, calling Django code for management commands.
    """
    os.environ["DJANGO_SETTINGS_MODULE"] = "pythonnest.djangoproject.settings"
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)