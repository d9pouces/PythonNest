# -*- coding: utf-8 -*-
import codecs
import hashlib
import json
from optparse import make_option
import os
import datetime
import shutil
from django.conf import settings

from django.core.management.base import BaseCommand
from django.utils.timezone import utc
from django.utils.translation import ugettext as _

from pythonnest.colors import cyan, red, yellow
from pythonnest.models import Synchronization, Package, Release, Classifier, Dependence, ReleaseDownload, PackageType
from pythonnest.views import DATE_FORMAT


__author__ = 'Matthieu Gallet'


class Command(BaseCommand):
    """Update local database from another Pypi server"""
    args = ''
    help = 'Export the database'
    option_list = BaseCommand.option_list + (
        make_option('--path', default='export', help='Folder to export to'),
        make_option('--force', default=False, action='store_true',
                    help='Force import even if a previous sync is missing'),
        make_option('--tag', default='export', help='Tag identifying this import'),
    )

    def handle(self, *args, **options):
        # first: determine the type of server
        obj = Synchronization.objects.get_or_create(destination='localhost', source=options['tag'])[0]
        if obj.last_serial is None:
            first_expected_serial = 0
            print(cyan(_('No previous sync')))
        else:
            first_expected_serial = obj.last_serial + 1
            print(cyan(_('Previous sync: serial %(syn)s') % {'syn': obj.last_serial}))
        base_path = os.path.abspath(options['path'])
        try:
            data = self.read_info(base_path, 'sync')
            packages = data['data']
            first_serial = data['meta']['first_id']
            last_serial = data['meta']['last_id']
        except KeyError:
            print(red(_('Invalid sync file')))
            return
        except ValueError:
            print(red(_('Invalid md5 data')))
            return
        except IOError:
            print(red(_('Invalid sync file')))
            return
        if first_serial > first_expected_serial:
            print(red(_('Missing synchronization between %(f)d and %(l)d') % {'f': first_expected_serial,
                                                                              'l': first_serial}))
            if not options['force']:
                return
        stop = False
        for package_name, releases in packages.items():
            p_path = os.path.join(base_path, package_name)
            package_data = self.read_info(p_path, 'package')
            package, created = Package.objects.get_or_create(name=package_name)
            self.set_attr(('name', 'author', 'author_email', 'maintainer', 'maintainer_email', 'home_page', 'license',
                           'summary',  'download_url', 'project_url', ),
                          package_data, package)
            package.save()
            for version, filenames in releases.items():
                r_path = os.path.join(base_path, package_name, version)
                release_data = self.read_info(r_path, 'release')
                release, created = Release.objects.get_or_create(package=package, version=version)
                self.set_attr(('version', 'stable_version', 'description', 'platform', 'keywords', 'docs_url', ),
                              release_data, release)
                release.classifiers.clear()
                for value in release_data.get('classifiers', []):
                    release.classifiers.add(Classifier.get(value))
                for attr_name in ('requires', 'requires_dist', 'provides', 'provides_dist', 'requires_external',
                                  'requires_python', 'obsoletes', 'obsoletes_dist', ):
                    getattr(release, attr_name).clear()
                    for value in release_data.get(attr_name, []):
                        getattr(release, attr_name).add(Dependence.get(value))
                release.save()
                for filename in filenames:
                    filepath = os.path.join(r_path, filename)
                    download_data = self.read_info(r_path, filename)
                    if ReleaseDownload.objects.filter(package=package, release=release, filename=filename).count() > 0:
                        print(yellow(_('Duplicate file: %(f)s') % {'f': filepath}))
                        continue
                    download = ReleaseDownload(package=package, release=release, filename=filename)

                    self.set_attr(('md5_digest', 'downloads', 'pack', 'has_sig', 'comment_text', 'python_version'),
                                  download_data, download)
                    download.package_type = PackageType.get(download_data.get('packagetype'))
                    dirname = os.path.dirname(download.abspath)
                    if not os.path.isdir(dirname):
                        os.makedirs(dirname)
                    shutil.copy2(filepath, download.abspath)
                    download.file = download.relpath
                    download.url = settings.MEDIA_URL + download.relpath
                    download.size = os.path.getsize(filepath)
                    if download_data.get('upload_time'):
                        download.upload_time = datetime.datetime.strptime(download_data['upload_time'], DATE_FORMAT)\
                            .replace(tzinfo=utc)
                    with open(filepath, 'rb') as file_d:
                        md5 = hashlib.md5(file_d.read()).hexdigest()
                    download.md5_digest = md5
                    if md5 != download_data.get('md5_digest'):
                        print(red(_('Corrupted file: %(f)s') % {'f': filepath}))
                        stop = True
                        break
                    download.log()
                if stop:
                    break
            if stop:
                break
        if not stop:
            Synchronization.objects.filter(id=obj.id).update(last_serial=last_serial)

    @staticmethod
    def read_info(dest_dir, prefix):
        with codecs.open(os.path.join(dest_dir, prefix + '.json'), 'r', encoding='utf-8') as json_fd:
            data = json.load(json_fd)
        with open(os.path.join(dest_dir, prefix + '.json'), 'rb') as json_fd:
            md5 = hashlib.md5(json_fd.read()).hexdigest()
        with codecs.open(os.path.join(dest_dir, prefix + '.md5'), 'r', encoding='utf-8') as md5_fd:
            if md5_fd.read() != md5:
                raise ValueError
        return data

    @staticmethod
    def set_attr(attr_list, src, dst):
        for attr_name in attr_list:
            if src.get(attr_name) is not None:
                setattr(dst, attr_name, src[attr_name])
