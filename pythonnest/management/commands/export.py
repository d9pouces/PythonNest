# -*- coding: utf-8 -*-
import codecs
import hashlib
import json
from argparse import ArgumentParser
from optparse import make_option
import os
import shutil

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _

from pythonnest.colors import cyan, yellow
from pythonnest.models import Synchronization, Log
from pythonnest.views import JSONDatetime


__author__ = 'Matthieu Gallet'


class Command(BaseCommand):
    """Update local database from another Pypi server"""
    args = ''
    help = 'Export the database'

    def add_arguments(self, parser):
        assert isinstance(parser, ArgumentParser)
        parser.add_argument('--path', default='export', help='Folder to export data to')
        parser.add_argument('--serial', type=int, default=None, help='Start from this serial')
        parser.add_argument('--tag', default='export', help='Tag identifying this export')

    def handle(self, *args, **options):
        # first: determine the type of server
        obj = Synchronization.objects.get_or_create(source='localhost', destination=options['tag'])[0]
        if isinstance(options['serial'], int):
            first_serial = options['serial']
            print(cyan(_('Dumping from serial %(syn)s') % {'syn': first_serial}))
        elif obj.last_serial is None:
            first_serial = 0
            print(cyan(_('No previous sync... Dumping all database')))
        else:
            first_serial = obj.last_serial
            print(cyan(_('Previous sync: serial %(syn)s') % {'syn': obj.last_serial}))
        packages = set()
        releases = set()
        result = {'data': {}}
        base_path = os.path.abspath(options['path'])
        last_serial = first_serial
        next_last_serial = -1
        for log in Log.objects.filter(id__gte=first_serial).order_by('id').select_related():
            p_path = os.path.join(base_path, log.package.name)
            if log.package.id not in packages:
                self.write_info(log.package.data(), p_path, 'package')
                result['data'][log.package.name] = {}
                packages.add(log.package.id)
            r_path = os.path.join(p_path, log.release.version)
            if log.release.id not in releases:
                self.write_info(log.release.data(), r_path, 'release')
                result['data'][log.package.name][log.release.version] = []
                releases.add(log.release.id)
            dst_path = os.path.join(r_path, log.download.filename)
            src_path = log.download.abspath
            shutil.copy2(src_path, dst_path)
            self.write_info(log.download.data(), r_path, log.download.filename)
            print(yellow(_('Adding %(fn)s (%(pk)s %(vn)s)') % {'pk': log.package.name, 'fn': log.download.filename,
                                                               'vn': log.release.version, }))
            result['data'][log.package.name][log.release.version].append(log.download.filename)
            last_serial = log.id
            next_last_serial = log.id + 1
        result['meta'] = {'first_id': first_serial, 'last_id': last_serial}
        self.write_info(result, base_path, 'sync')
        Synchronization.objects.filter(id=obj.id).update(last_serial=next_last_serial)

    @staticmethod
    def write_info(data, dest_dir, prefix):
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        with codecs.open(os.path.join(dest_dir, prefix + '.json'), 'w', encoding='utf-8') as json_fd:
            json.dump(data, json_fd, ensure_ascii=False, cls=JSONDatetime, indent=2)
        with open(os.path.join(dest_dir, prefix + '.json'), 'rb') as json_fd:
            md5 = hashlib.md5(json_fd.read()).hexdigest()
        with codecs.open(os.path.join(dest_dir, prefix + '.md5'), 'w', encoding='utf-8') as md5_fd:
            md5_fd.write(md5)
