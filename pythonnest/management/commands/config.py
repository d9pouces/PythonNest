import os
from django.conf import settings
from django.core.management import BaseCommand
from django.utils.translation import ugettext as _


__author__ = 'flanker'


class Command(BaseCommand):
    help = _('display the location of the main configuration file')

    def handle(self, *args, **options):
        print(os.path.abspath(settings.CONFIG_FILES[-1]))