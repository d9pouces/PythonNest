# -*- coding: utf-8 -*-
import gzip
import hashlib
from argparse import ArgumentParser
from optparse import make_option
import os
import socket
import time
from urllib.error import URLError
import urllib.request
import xmlrpc.client
import http.client
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.timezone import utc
from django.utils.translation import ugettext as _

from pythonnest.colors import cyan, green, yellow
from pythonnest.models import Synchronization, Package, ObjectCache, Release, Classifier, Dependence, ReleaseDownload, \
    PackageType, PackageRole, ReleaseMiss


class DownloadException(Exception):
    pass


class MD5SumException(Exception):
    pass


__author__ = 'Matthieu Gallet'


class ProxiedTransport(xmlrpc.client.Transport):
    def set_proxy(self, proxy):
        # noinspection PyAttributeOutsideInit
        self.proxy = proxy

    def set_protocol(self, protocol='http'):
        # noinspection PyAttributeOutsideInit
        self.protocol = 'https' if protocol.startswith('https') else 'http'

    def make_connection(self, host):
        # noinspection PyAttributeOutsideInit
        self.realhost = host
        if self.proxy.startswith('https'):
            chost, self._extra_headers, x509 = self.get_host_info(self.proxy)
            connection = http.client.HTTPSConnection(chost, None, **(x509 or {}))
        else:
            connection = http.client.HTTPConnection(self.proxy)
        return connection

    def send_request(self, host, handler, request_body, debug):
        connection = self.make_connection(host)
        headers = self._extra_headers[:]
        if debug:
            connection.set_debuglevel(1)
        proxied_handler = '%s://%s%s' % (self.protocol, self.realhost, handler)
        if self.accept_gzip_encoding and gzip:
            connection.putrequest("POST", proxied_handler, skip_accept_encoding=True)
            headers.append(("Accept-Encoding", "gzip"))
        else:
            connection.putrequest("POST", proxied_handler)
        connection.putheader('Host', self.realhost)
        headers.append(("Content-Type", "text/xml"))
        headers.append(("User-Agent", self.user_agent))
        self.send_headers(connection, headers)
        self.send_content(connection, request_body)
        return connection


class Command(BaseCommand):
    """Update local database from another Pypi server"""
    # pylint: disable=R0912
    # pylint: disable=R0915
    args = ''
    help = 'Update the local database from another Pypi server'

    def add_arguments(self, parser):
        assert isinstance(parser, ArgumentParser)
        parser.add_argument('--url', default='https://pypi.python.org/pypi',
                            help='Server to sync. against (default: https://pypi.python.org/pypi)'),
        parser.add_argument('--limit', type=int, default=None, help='Do not download more thant --limit archives'),
        parser.add_argument('--serial', type=int, default=None, help='Start from this serial'),
        parser.add_argument('--retry', type=int, default=5, help='Max retry count (default 5)'),
        parser.add_argument('--timeout', type=int, default=10, help='Timeout for network operations (default 10s)'),
        parser.add_argument('--nocontinue', action='store_true', default=False, help='Stop after error'),
        parser.add_argument('--package', action='store', default=None,
                            help='Download all releases of a single package'),
        parser.add_argument('--latest', action='store_true', default=False,
                            help='Download the latest release of all packages'),
        parser.add_argument('--init-all', action='store_true', default=False,
                            help='Download all releases of all packages (very long initial sync!)'),

    def __init__(self):
        super(Command, self).__init__()
        self.user_cache = ObjectCache(lambda key_: User.objects.get_or_create(username=key_)[0])
        self.package_cache = ObjectCache(lambda key_: Package.objects.get_or_create(name=key_)[0])
        self.client = None
        self.retry = 5
        self.error_list = []

    def connect(self, url):
        self.client = xmlrpc.client.ServerProxy(url)

    def download_release_file(self, path, release_url):
        md5_check = hashlib.md5()
        with urllib.request.urlopen(release_url['url'], None, 5) as in_fd:
            size = 0
            with open(path, 'wb') as out_fd:
                data = in_fd.read(40960)
                while data:
                    out_fd.write(data)
                    size += len(data)
                    md5_check.update(data)
                    data = in_fd.read(40960)
        if md5_check.hexdigest() != release_url.get('md5_digest'):
            os.remove(path)
            self.stderr.write((_('Error while downloading %(url)s [invalid md5 digest]') %
                               {'url': release_url['url']}))
            raise MD5SumException

    def download_release(self, package_name, version):
        """ download all files attached to a given release of a given package
        """
        downloaded_files = 0
        package = self.package_cache.get(package_name)
        values = {'p': package_name, 'v': version}
        self.stdout.write(yellow(_('release data (%(p)s, %(v)s)') % values))
        try:
            release_data = self.try_download(self.client.release_data,
                                             _('Unable to get release date of %(p)s-%(v)s') % values, package_name,
                                             version)
            update_kwargs = {}
            # update package object with latest metadata
            for attr_name in ('home_page', 'license', 'summary', 'download_url', 'project_url',
                              'author', 'author_email', 'maintainer', 'maintainer_email'):
                if release_data.get(attr_name):
                    update_kwargs[attr_name] = release_data[attr_name][0:450]
            if update_kwargs:
                Package.objects.filter(id=package.id).update(**update_kwargs)
            self.stdout.write(yellow(_('package roles (%(p)s, %(v)s)') % values))
            roles = self.try_download(self.client.package_roles, _('Unable to get roles for %(p)s-%(v)s') % values,
                                      package_name)
            # roles of persons
            PackageRole.objects.filter(package=package).delete()
            package_roles = [PackageRole(package=package,
                                         role=PackageRole.OWNER if role == 'Owner' else PackageRole.MAINTAINER,
                                         user=self.user_cache.get(username)) for (role, username) in roles]
            PackageRole.objects.bulk_create(package_roles)
        except DownloadException:
            self.error_list.append((package_name, version))
            return 0

        # update release object
        release = Release.objects.get_or_create(package=package, version=version)[0]
        for attr_name in ('stable_version', 'description', 'platform', 'docs_url', 'project_url', 'keywords'):
            if release_data.get(attr_name):
                setattr(package, attr_name, release_data.get(attr_name)[0:450])
        release.is_hidden = release_data.get('_pypi_hidden', False)
        for attr_name in ('classifiers', 'requires', 'requires_dist', 'provides', 'provides_dist',
                          'obsoletes', 'obsoletes_dist', 'requires_external', 'requires_python'):
            cls = Classifier if attr_name == 'classifiers' else Dependence
            if release_data.get(attr_name):
                getattr(release, attr_name).clear()
                for key in release_data[attr_name]:
                    getattr(release, attr_name).add(cls.get(key))
        release.save()

        # update archives
        self.stdout.write(yellow(_('release urls (%(p)s, %(v)s)') % values))
        try:
            release_urls = self.try_download(self.client.release_urls,
                                             _('Unable to get release urls of %(p)s-%(v)s') % values,
                                             package_name, version)
        except DownloadException:
            return 0
        for release_url in release_urls:
            md5_digest = release_url.get('md5_digest')
            c = ReleaseDownload.objects.filter(md5_digest=md5_digest, package=package, release=release).count()
            if c > 0 or not release_url.get('url') or not release_url.get('filename'):
                continue
            self.stdout.write(green(_('Downloading %(url)s') % {'url': release_url['url']}))
            filename = release_url['filename']
            download = ReleaseDownload(package=package, release=release, filename=filename)
            path = download.abspath
            path_dirname = os.path.dirname(path)
            if not os.path.isdir(path_dirname):
                os.makedirs(path_dirname)
            try:
                self.try_download(self.download_release_file,
                                  _('Unable to download file %(url)s') % {'url': release_url},
                                  path, release_url)
            except DownloadException:
                ReleaseMiss.objects.get_or_create(release=release)
                self.error_list.append((package_name, version))
                continue
            download.file = download.relpath
            download.url = settings.MEDIA_URL + download.relpath
            if release_url.get('packagetype'):
                download.package_type = PackageType.get(release_url.get('packagetype'))
            if release_url.get('upload_time'):
                download.upload_time = datetime.datetime.strptime(release_url['upload_time'].value, "%Y%m%dT%H:%M:%S") \
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
        sync_obj = Synchronization.objects.get_or_create(source=options['url'], destination='localhost')[0]
        self.retry = options['retry']
        socket.setdefaulttimeout(options['timeout'])
        download_limit = 0 if not options['limit'] else options['limit']
        if isinstance(options['serial'], int):
            first_serial = options['serial']
            init = False
            self.stdout.write(cyan(_('Download from serial %(syn)s') % {'syn': first_serial}))
        elif sync_obj.last_serial is None or options['init_all']:
            first_serial = 0
            init = True
            self.stdout.write(cyan(_('No previous sync... Initializing database')))
        else:
            self.stdout.write(cyan(_('Previous sync: serial %(syn)s') % {'syn': sync_obj.last_serial}))
            first_serial = sync_obj.last_serial
            init = False
        self.connect(options['url'])
        last_serial = None

        if options['package']:
            # get all releases of the given package
            package_name = options['package']
            self.stdout.write(cyan(_('Downloading all versions of %(pkg)s') % {'pkg': package_name}))
            try:
                versions = self.try_download(self.client.package_releases,
                                             _('Unable to get releases of %(pkg)s') % {'pkg': package_name},
                                             package_name, True)
            except DownloadException:
                versions = []
            for version in versions:
                self.download_release(package_name, version)
        elif not options['latest'] and (not init or options['init_all']):
            # get all releases from the given serial
            last_serial = first_serial
            try:
                modified_packages = self.try_download(self.client.changelog_since_serial,
                                                      _('Unable to download changelog'), first_serial + 1)
            except DownloadException:
                modified_packages = []
            counter = 0
            for (package_name, version, timestamp, action, serial) in modified_packages:
                last_serial = max(serial, last_serial)
                if counter >= download_limit > 0:
                    break
                if version is None:
                    continue
                self.stdout.write(cyan(_('Found %(pkg)s-%(vsn)s') % {'pkg': package_name, 'vsn': version}))
                counter += self.download_release(package_name, version)
        else:
            # init: get the last version of all packages
            try:
                last_serial = self.try_download(self.client.changelog_last_serial, _('Unable to download changelog'))
                packages = self.try_download(self.client.list_packages, _('Unable to list packages'))
            except DownloadException:
                return
            counter = 0
            for package_name in packages:
                if counter >= download_limit > 0:
                    break
                self.stdout.write(cyan(_('Found %(pkg)s') % {'pkg': package_name}))
                self.stdout.write(yellow(_('package releases (%(p)s)') % {'p': package_name}))
                try:
                    versions = self.try_download(self.client.package_releases,
                                                 _('Unable to get releases of %(pkg)s') % {'pkg': package_name},
                                                 package_name)
                except DownloadException:
                    continue
                versions = [x for x in versions if x]
                if not versions:
                    continue
                version = versions[0]
                self.stdout.write(cyan(_('Found %(pkg)s-%(vsn)s') % {'pkg': package_name, 'vsn': version}))
                counter += self.download_release(package_name, version)
        if last_serial is not None:
            Synchronization.objects.filter(id=sync_obj.id).update(last_serial=last_serial)
        for package_name, version in self.error_list:
            self.stderr.write((_('Unable to download %(p)s-%(v)s') % {'p': package_name, 'v': version}))

    def try_download(self, action, error_message, *args, **kwargs):
        """ perform a network connection and retry several times if an error happens. All errors are displayed.
        """
        no_timeout = 0
        while no_timeout < self.retry:
            try:
                return action(*args, **kwargs)
            except URLError:
                self.stderr.write(_('%(msg)s [URL error]') % {'msg': error_message})
                time.sleep(3)
                no_timeout += 1
            except socket.timeout:
                self.stderr.write(_('%(msg)s [socket timeout]') % {'msg': error_message})
                time.sleep(3)
                no_timeout += 1
            except socket.gaierror:
                self.stderr.write(_('%(msg)s [Gai error]') % {'msg': error_message})
                time.sleep(2)
                no_timeout += 1
            except xmlrpc.client.ProtocolError:
                self.stderr.write(_('%(msg)s [XMLRPC Protocol error]') % {'msg': error_message})
                time.sleep(2)
                no_timeout += 1
            except MD5SumException:
                self.stderr.write(_('%(msg)s [Invalid md5 sum]') % {'msg': error_message})
                time.sleep(2)
                no_timeout += 1
            except Exception as e:
                self.stderr.write(_('%(msg)s [Unexpected exception %(exc)s]') % {'msg': error_message, 'exc': e})
                time.sleep(2)
                no_timeout += 1
        raise DownloadException
