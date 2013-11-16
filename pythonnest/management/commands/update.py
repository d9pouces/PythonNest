# -*- coding: utf-8 -*-
import hashlib
from optparse import make_option
import os
import socket
import time
from urllib.error import URLError
import urllib.request
import xmlrpc.client
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.timezone import utc
from django.utils.translation import ugettext as _

from pythonnest.colors import cyan, green, red, yellow
from pythonnest.models import Synchronization, Package, ObjectCache, Release, Classifier, Dependence, ReleaseDownload,\
    PackageType, PackageRole, ReleaseMiss


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
        make_option('--limit', type=int, default=None, help='Do not download more thant --limit archives'),
        make_option('--serial', type=int, default=None, help='Start from this serial'),
        make_option('--retry', type=int, default=5, help='Max retry count (default 5)'),
        make_option('--timeout', type=int, default=10, help='Timeout for network operations (default 10s)'),
        make_option('--init-all', action='store_true', default=False,
                    help='Force the download of all releases of all packages (very long initial sync!)'),
    )

    def __init__(self):
        super(Command, self).__init__()
        self.user_cache = ObjectCache(lambda key_: User.objects.get_or_create(username=key_)[0])
        self.package_cache = ObjectCache(lambda key_: Package.objects.get_or_create(name=key_)[0])
        self.client = None
        self.retry = 5

    def connect(self, url):
        self.client = xmlrpc.client.ServerProxy(url)

    def download_release(self, package_name, version):
        downloaded_files = 0
        package = self.package_cache.get(package_name)
        print(yellow(_('release data (%(p)s, %(v)s)') % {'p': package_name, 'v': version}))
        release_data = self.client.release_data(package_name, version)
        # update package object
        for attr_name in ('home_page', 'license', 'summary', 'download_url', 'project_url',
                          'author', 'author_email', 'maintainer', 'maintainer_email'):
            if release_data.get(attr_name):
                setattr(package, attr_name, release_data.get(attr_name))
        package.save()
        print(yellow(_('package roles (%(p)s, %(v)s)') % {'p': package_name, 'v': version}))
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
        print(yellow(_('release urls (%(p)s, %(v)s)') % {'p': package_name, 'v': version}))
        release_urls = self.client.release_urls(package_name, version)
        for release_url in release_urls:
            md5_digest = release_url.get('md5_digest')
            c = ReleaseDownload.objects.filter(md5_digest=md5_digest, package=package, release=release).count()
            if c > 0 or not release_url.get('url') or not release_url.get('filename'):
                continue
            print(green(_('Downloading %(url)s') % {'url': release_url['url']}))
            filename = release_url['filename']
            download = ReleaseDownload(package=package, release=release, filename=filename)
            no_timeout = 0
            while no_timeout < self.retry:
                try:
                    path = download.abspath
                    with urllib.request.urlopen(release_url['url'], None, 5) as in_fd:
                        path_dirname = os.path.dirname(path)
                        md5_check = hashlib.md5()
                        size = 0
                        if not os.path.isdir(path_dirname):
                            os.makedirs(path_dirname)
                        with open(path, 'wb') as out_fd:
                            data = in_fd.read(4096)
                            while data:
                                out_fd.write(data)
                                size += len(data)
                                md5_check.update(data)
                                data = in_fd.read(4096)
                    if md5_check.hexdigest() != release_url.get('md5_digest'):
                        os.remove(path)
                        print(red(_('Error while downloading %(url)s [invalid md5 digest]') % {'url': release_url['url']}))
                        no_timeout += 1
                        continue
                    download.file = download.relpath
                    download.url = settings.MEDIA_URL + download.relpath
                    break
                except URLError:
                    print(red(_('Error while downloading %(url)s') % {'url': release_url['url']}))
                    ReleaseMiss.objects.get_or_create(release=release)
                    no_timeout = self.retry
                    break
                except socket.gaierror:
                    print(red(_('Error while downloading %(url)s [GAI error]') % {'url': release_url['url']}))
                    ReleaseMiss.objects.get_or_create(release=release)
                    time.sleep(2)
                    no_timeout += 1
                except socket.timeout:
                    print(red(_('Error while downloading %(url)s [socket timeout]') % {'url': release_url['url']}))
                    ReleaseMiss.objects.get_or_create(release=release)
                    time.sleep(2)
                    no_timeout += 1
            if no_timeout >= self.retry:
                continue
            if release_url.get('packagetype'):
                download.package_type = PackageType.get(release_url.get('packagetype'))
            if release_url.get('upload_time'):
                download.upload_time = datetime.datetime.strptime(release_url['upload_time'].value, "%Y%m%dT%H:%M:%S")\
                    .replace(tzinfo=utc)
            for attr_name in ('filename', 'size', 'downloads', 'has_sig', 'python_version',
                              'comment_text', 'md5_digest'):
                if release_url.get(attr_name):
                    setattr(download, attr_name, release_url[attr_name])
            download.log()
            downloaded_files += 1
        ReleaseMiss.objects.filter(release=release).delete()
        return downloaded_files

    def handle(self, *args, **options):
        # first: determine the type of server
        obj = Synchronization.objects.get_or_create(source=options['url'], destination='localhost')[0]
        self.retry = options['retry']
        socket.setdefaulttimeout(options['timeout'])
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
                no_timeout = 0
                while no_timeout < self.retry:
                    try:
                        counter += self.download_release(package_name, version)
                        break
                    except socket.timeout:
                        print(red(_('Timeout with %(p)s-%(v)s [socket timeout]') % {'p': package_name, 'v': version}))
                        time.sleep(3)
                        no_timeout += 1
                    except socket.gaierror:
                        print(red(_('Gai error with %(p)s-%(v)s') % {'p': package_name, 'v': version}))
                        time.sleep(2)
                        no_timeout += 1
                    except xmlrpc.client.ProtocolError:
                        print(red(_('Protocol error with %(p)s-%(v)s') % {'p': package_name, 'v': version}))
                        time.sleep(2)
                        no_timeout += 1
        else:
            last_serial = self.client.changelog_last_serial()
            packages = self.client.list_packages()
            counter = 0
            for package_name in packages:
                if options['limit'] is not None and counter >= options['limit']:
                    break
                print(cyan(_('Found %(pkg)s') % {'pkg': package_name}))
                no_timeout = 0
                while no_timeout < self.retry:
                    try:
                        print(yellow(_('package releases (%(p)s)') % {'p': package_name}))
                        versions = self.client.package_releases(package_name)
                        versions = [x for x in versions if x]
                        if not versions:
                            break
                        version = versions[0]
                        print(cyan(_('Found %(pkg)s-%(vsn)s') % {'pkg': package_name, 'vsn': version}))
                        counter += self.download_release(package_name, version)
                        break
                    except socket.timeout:
                        print(red(_('Timeout with %(p)s-%(v)s [socket timeout]') % {'p': package_name, 'v': version}))
                        time.sleep(3)
                        no_timeout += 1
                    except socket.gaierror:
                        print(red(_('Gai error with %(p)s-%(v)s') % {'p': package_name, 'v': version}))
                        time.sleep(2)
                        no_timeout += 1
                    except xmlrpc.client.ProtocolError:
                        print(red(_('Protocol error with %(p)s-%(v)s') % {'p': package_name, 'v': version}))
                        time.sleep(2)
                        no_timeout += 1

        Synchronization.objects.filter(id=obj.id).update(last_serial=last_serial)
