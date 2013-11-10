# -*- coding: utf-8 -*-
from optparse import make_option
import os
import socket
from urllib.error import URLError
import urllib.request
import xmlrpc.client
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.timezone import utc
from django.utils.translation import ugettext as _

from pythonnest.colors import cyan, green, red
from pythonnest.models import Synchronization, Package, ObjectCache, Release, Classifier, Dependence, ReleaseDownload,\
    PackageType, release_download_path, PackageRole


__author__ = "flanker"


class Command(BaseCommand):
    """Update local database from another Pypi server"""
    # pylint: disable=R0912
    # pylint: disable=R0915
    args = ''
    help = 'Update the local database from another Pypi server'
    option_list = BaseCommand.option_list + (
        make_option('--url', default='http://pypi.python.org/pypi',
                    help='Server to sync. against (default: http://pypi.python.org/pypi)'),
        make_option('--limit', type=int, default=None,
                    help='Do not download more thant --limit archives'),
        make_option('--serial', type=int, default=None,
                    help='Start from this serial'),
        make_option('--init-all', action='store_true', default=False,
                    help='Force the download of all releases of all packages (very long initial sync!)'),
    )

    def __init__(self):
        super(Command, self).__init__()
        self.user_cache = ObjectCache(lambda key_: User.objects.get_or_create(username=key_)[0])
        self.package_cache = ObjectCache(lambda key_: Package.objects.get_or_create(name=key_)[0])
        self.media_root_length = len(settings.MEDIA_ROOT)
        if settings.MEDIA_ROOT[-1:] != '/':
            self.media_root_length += 1
        self.client = None

    def connect(self, url):
        self.client = xmlrpc.client.ServerProxy(url)

    def download_release(self, package_name, version):
        downloaded_files = 0
        package = self.package_cache.get(package_name)
        release_data = self.client.release_data(package_name, version)
        # update package object
        for attr_name in ('home_page', 'license', 'summary', 'download_url', 'project_url',
                          'author', 'author_email', 'maintainer', 'maintainer_email'):
            if release_data.get(attr_name):
                setattr(package, attr_name, release_data.get(attr_name))
        package.save()
        roles = self.client.package_roles(package_name)
        PackageRole.objects.filter(package=package).delete()
        for (role, username) in roles:
            role_int = PackageRole.OWNER if role == 'Owner' else PackageRole.MAINTAINER
            PackageRole(package=package, role=role_int, user=self.user_cache.get(username)).save()

        # update release object
        release = Release.objects.get_or_create(package=package, version=version)[0]
        for attr_name in ('stable_version', 'description', 'platform', 'docs_url', 'project_url', 'keywords'):
            if release_data.get(attr_name):
                setattr(package, attr_name, release_data.get(attr_name))
        release.is_hidden = release_data.get('_pypi_hidden', False)
        for attr_name in ('classifiers', 'requires', 'requires_dist', 'provides', 'provides_dist',
                          'obsoletes', 'obsoletes_dist', 'requires_external', 'requires_python'):
            cls = Classifier if attr_name == 'classifiers' else Dependence
            if release_data.get(attr_name):
                getattr(release, attr_name).clear()
                for key in release_data[attr_name]:
                    getattr(release, attr_name).add(cls.get(key))
        release.save()

        #update archives
        release_urls = self.client.release_urls(package_name, version)
        for release_url in release_urls:
            md5_digest = release_url.get('md5_digest')
            c = ReleaseDownload.objects.filter(md5_digest=md5_digest, package=package, release=release).count()
            if c > 0 or not release_url.get('url') or not release_url.get('filename'):
                continue
            print(green(_('Downloading %(url)s') % {'url': release_url['url']}))
            download = ReleaseDownload(package=package, release=release)
            try:
                path = settings.MEDIA_ROOT + '/' + release_download_path(download, release_url['filename'])
                with urllib.request.urlopen(release_url['url'], None, 5) as in_fd:
                    path_dirname = os.path.dirname(path)
                    if not os.path.isdir(path_dirname):
                        os.makedirs(path_dirname)
                    with open(path, 'wb') as out_fd:
                        data = in_fd.read(4096)
                        while data:
                            out_fd.write(data)
                            data = in_fd.read(4096)
                download.file = path[self.media_root_length:]
                download.url = settings.MEDIA_URL + path[self.media_root_length:]
            except URLError:
                print(red(_('Error while downloading %(url)s') % {'url': release_url['url']}))
                continue
            except socket.timeout:
                print(red(_('Error while downloading %(url)s') % {'url': release_url['url']}))
                continue
            if release_url.get('packagetype'):
                download.package_type = PackageType.get(release_url.get('packagetype'))
            else:
                download.package_type = PackageType.get('UNKNOWN')
            if release_url.get('upload_time'):
                upload_time = datetime.datetime.strptime(release_url['upload_time'].value, "%Y%m%dT%H:%M:%S") \
                    .replace(tzinfo=utc)
                download.upload_time = upload_time
            for attr_name in ('filename', 'size', 'downloads', 'has_sig', 'python_version',
                              'comment_text', 'md5_digest'):
                if release_url.get(attr_name):
                    setattr(download, attr_name, release_url[attr_name])
            download.log()
            downloaded_files += 1
        return downloaded_files

    def handle(self, *args, **options):
        # first: determine the type of server
        obj = Synchronization.objects.get_or_create(source=options['url'], destination='localhost')[0]
        if isinstance(options['serial'], int):
            first_serial = options['serial']
            init = False
            print(cyan(_('Download from serial %(syn)s') % {'syn': first_serial}))
        elif obj.last_serial is None or options['init_all']:
            first_serial = 0
            init = True
            print(cyan(_('No previous sync... Initializing database')))
        else:
            print(cyan(_('Previous sync: serial %(syn)s') % {'syn': obj.last_serial}))
            first_serial = obj.last_serial
            init = False
        self.connect(options['url'])
        if not init or options['init_all']:
            last_serial = first_serial
            modified_packages = self.client.changelog_since_serial(first_serial + 1)
            counter = 0
            for (package_name, version, timestamp, action, serial) in modified_packages:
                last_serial = max(serial, last_serial)
                if options['limit'] is not None and counter >= options['limit']:
                    break
                if version is None:
                    continue
                print(cyan(_('Found %(pkg)s-%(vsn)s') % {'pkg': package_name, 'vsn': version}))
                counter += self.download_release(package_name, version)
        else:
            last_serial = self.client.changelog_last_serial()
            packages = self.client.list_packages()
            counter = 0
            for package_name in packages:
                if options['limit'] is not None and counter >= options['limit']:
                    break
                print(cyan(_('Found %(pkg)s') % {'pkg': package_name}))
                versions = self.client.package_releases(package_name)
                versions = [x for x in versions if x]
                if not versions:
                    continue
                version = versions[0]
                print(cyan(_('Found %(pkg)s-%(vsn)s') % {'pkg': package_name, 'vsn': version}))
                counter += self.download_release(package_name, version)

        Synchronization.objects.filter(id=obj.id).update(last_serial=last_serial)
