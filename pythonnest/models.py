# -*- coding: utf-8 -*-
"""Define your models in this module.

Models are standard Python classes which inherits from
:class:`django.db.models.Model`. A model represents a SQL table.

Documentation can be found at .

"""
from heapq import heappop, heappush
import os
import uuid
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
import time
import unicodedata

__author__ = 'Matthieu Gallet'


def normalize_str(s):
    s = s.replace('_', '-')
    return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII').lower()


class ObjectCache(object):

    def __init__(self, cache_miss_fn, limit=1000):
        self.obj_key = {}
        self.key_list = []
        self.limit = limit
        self.cache_miss_fn = cache_miss_fn

    def get(self, key):
        if key in self.obj_key:
            return self.obj_key[key]
        obj = self.cache_miss_fn(key)
        self.obj_key[key] = obj
        heappush(self.key_list, key)
        if len(self.key_list) > self.limit:
            key = heappop(self.key_list)
            del self.obj_key[key]
        return obj


class Synchronization(models.Model):
    """
    Keeps informations about synchronizations
    """

    source = models.CharField(_('Source'), blank=True, db_index=True, default='', max_length=455)
    destination = models.CharField(_('Destination'), blank=True, db_index=True, default='', max_length=455)
    last_serial = models.IntegerField(_('Last synchronized serial'), blank=True, null=True, default=None)
    creation = models.DateTimeField(_('creation'), db_index=True, auto_now_add=True)
    modification = models.DateTimeField(_('modification'), db_index=True, auto_now=True)

    class Meta:
        verbose_name = _('Synchronization')
        verbose_name_plural = _('Synchronizations')

    def __str__(self):
        return ugettext('%(s)s -> %(d)s') % {'s': self.source, 'd': self.destination, }


class CachedName(models.Model):
    name = models.CharField(_('Classifier'), db_index=True, max_length=455)
    creation = models.DateTimeField(_('creation'), db_index=True, auto_now_add=True)
    modification = models.DateTimeField(_('modification'), db_index=True, auto_now=True)
    __cache = None

    @classmethod
    def get(cls, name):
        if cls.__cache is None:
            cls.__cache = ObjectCache(lambda key: cls.objects.get_or_create(name=key)[0])
        return cls.__cache.get(name)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Classifier(CachedName):
    __cache = None


class Dependence(CachedName):
    __cache = None


class PackageType(CachedName):
    __cache = None


class Package(models.Model):
    name = models.CharField(_('package name'), db_index=True, blank=True, default='', max_length=455)
    normalized_name = models.CharField(_('normalized name'), db_index=True, blank=True, default='', max_length=455)
    author = models.CharField(_('author'), db_index=True, blank=True, null=True, max_length=455)
    author_email = models.CharField(_('author email'), db_index=True, blank=True, null=True, max_length=455)
    maintainer = models.CharField(_('maintainer'), db_index=True, blank=True, null=True, max_length=455)
    maintainer_email = models.CharField(_('maintainer email'), db_index=True, blank=True, null=True, max_length=455)
    home_page = models.URLField(_('home page'), db_index=True, blank=True, default='')
    license = models.CharField(_('license'), db_index=True, blank=True, default='UNKNOWN', max_length=455)
    summary = models.TextField(_('summary'), blank=True, default='')
    download_url = models.URLField(_('download url'), db_index=True, blank=True, default='')
    project_url = models.URLField(_('project url'), db_index=True, blank=True, default='')
    creation = models.DateTimeField(_('creation'), db_index=True, auto_now_add=True)
    modification = models.DateTimeField(_('modification'), db_index=True, auto_now=True)
    group = models.ForeignKey(Group, verbose_name=_('restrict to this group'), db_index=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.normalized_name = normalize_str(self.name)
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def data(self):
        result = {}
        for attr_name in ('name', 'author', 'author_email', 'maintainer', 'maintainer_email', 'home_page', 'license',
                          'summary',  'download_url', 'project_url', ):
            result[attr_name] = getattr(self, attr_name)
        return result

    def is_admin(self, user):
        if user.is_anonymous():
            return False
        if user.is_superuser:
            return True
        return PackageRole.objects.filter(package=self, user=user, role=PackageRole.OWNER).count() > 1

    def is_maintainer(self, user):
        if user.is_anonymous():
            return False
        if user.is_superuser:
            return True
        return PackageRole.objects.filter(package=self, user=user).count() > 1


class PackageRole(models.Model):
    OWNER = 1
    MAINTAINER = 2
    ROLES = ((OWNER, _('owner')), (MAINTAINER, _('maintainer')))
    role = models.IntegerField(_('role'), db_index=True, choices=ROLES, default=OWNER)
    user = models.ForeignKey(User, verbose_name=_('user'), db_index=True)
    package = models.ForeignKey(Package, verbose_name=_('package'), db_index=True)

    def __str__(self):
        return '%s - %s' % (self.user.username, self.package.name)


class Release(models.Model):
    package = models.ForeignKey(Package, db_index=True)
    version = models.CharField(_('version name'), db_index=True, blank=True, null=True, default='', max_length=455)
    stable_version = models.CharField(_('stable version name'), db_index=True, null=True, blank=True, default='',
                                      max_length=455)
    description = models.TextField(_('Description'), blank=True, default='', null=True)
    platform = models.CharField(_('platform'), db_index=True, blank=True, null=True, default='UNKNOWN', max_length=25)
    keywords = models.CharField(_('keywords'), db_index=True, blank=True, null=True, default='', max_length=455)
    classifiers = models.ManyToManyField(Classifier, db_index=True, blank=True)
    requires = models.ManyToManyField(Dependence, db_index=True, blank=True, related_name='dep_requires')
    requires_dist = models.ManyToManyField(Dependence, db_index=True, blank=True, related_name='dep_requires_dist')
    provides = models.ManyToManyField(Dependence, db_index=True, blank=True, related_name='dep_provides')
    provides_dist = models.ManyToManyField(Dependence, db_index=True, blank=True, related_name='dep_provides_dist')
    obsoletes = models.ManyToManyField(Dependence, db_index=True, blank=True, related_name='dep_obsoletes')
    obsoletes_dist = models.ManyToManyField(Dependence, db_index=True, blank=True, related_name='dep_obsoletes_dist')
    requires_external = models.ManyToManyField(Dependence, db_index=True, blank=True, related_name='dep_requires_external')
    requires_python = models.ManyToManyField(Dependence, db_index=True, blank=True, related_name='dep_requires_python')
    docs_url = models.URLField(_('docs url'), db_index=True, blank=True, default='', null=True)
    creation = models.DateTimeField(_('creation'), db_index=True, auto_now_add=True)
    modification = models.DateTimeField(_('modification'), db_index=True, auto_now=True)
    is_hidden = models.BooleanField(_('Is hidden'), db_index=True, default=False)
    PACKAGE_ATTR = {'name', 'home_page', 'license', 'summary', 'download_url', 'project_url', 'author', 'author_email',
                    'maintainer', 'maintainer_email'}

    def __getattr__(self, item):
        if item in self.PACKAGE_ATTR:
            return getattr(self.package, item)
        return super(Release, self).__getattr__(item)

    def __str__(self):
        return '{0}-{1}'.format(self.package.name, self.version)

    def data(self):
        result = {}
        for attr_name in ('name', 'version', 'stable_version', 'author', 'author_email', 'maintainer',
                          'maintainer_email', 'home_page', 'license', 'summary', 'description',
                          'platform', 'download_url', 'project_url', 'keywords', 'docs_url', ):
            result[attr_name] = getattr(self, attr_name)
        for attr_name in ('classifiers', 'requires', 'requires_dist', 'provides', 'provides_dist', 'requires_external',
                          'requires_python', 'obsoletes', 'obsoletes_dist', ):
            result[attr_name] = [x.name for x in getattr(self, attr_name).all()]
        return result


def release_download_path(obj, filename):
    if not obj.uid:
        obj.uid = str(uuid.uuid1())
    return 'downloads/' + '/'.join(obj.uid[0:4]) + '/' + filename

MEDIA_ROOT_LEN = len(settings.MEDIA_ROOT)
if settings.MEDIA_ROOT[-1:] != '/':
    MEDIA_ROOT_LEN += 1


class ReleaseMiss(models.Model):
    release = models.ForeignKey(Release, db_index=True)

    def __str__(self):
        return str(self.release)


class ReleaseDownload(models.Model):
    package = models.ForeignKey(Package, db_index=True, null=True, blank=True)
    release = models.ForeignKey(Release, db_index=True)
    uid = models.CharField(_('UID'), db_index=True, max_length=40, blank=True, default='')
    url = models.CharField(_('URL'), db_index=True, max_length=455, blank=True, default='')
    package_type = models.ForeignKey(PackageType, db_index=True, null=True, blank=True, default=None)
    filename = models.CharField(_('Filename'), db_index=True, max_length=455)
    file = models.FileField(_('File'), db_index=True, max_length=455, upload_to=release_download_path)
    size = models.IntegerField(_('Size'), db_index=True, blank=True, default=0)
    md5_digest = models.CharField(_('MD5'), db_index=True, max_length=40, blank=True, default='')
    downloads = models.IntegerField(_('Downloads'), db_index=True, blank=True, default=0)
    has_sig = models.BooleanField(_('Has signature'), db_index=True, default=False)
    python_version = models.CharField(_('Python version'), db_index=True, max_length=355, blank=True, default='any')
    comment_text = models.TextField(_('Comment'), blank=True, default='')
    upload_time = models.DateTimeField(_('Upload time'), blank=True, null=True, default=None, db_index=True)
    creation = models.DateTimeField(_('creation'), db_index=True, auto_now_add=True)
    modification = models.DateTimeField(_('modification'), db_index=True, auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.uid:
            self.uid = str(uuid.uuid1())
        if not self.package:
            self.package = self.release.package
        if self.file and not self.url:
            self.url = settings.MEDIA_URL + self.file.name[MEDIA_ROOT_LEN:]
        super(ReleaseDownload, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                          update_fields=update_fields)

    def log(self, action=''):
        self.save()
        Log(package=self.package, release=self.release, action=action, download=self).save()

    def __str__(self):
        return self.filename

    @property
    def packagetype(self):
        return 'archive' if not self.package_type else self.package_type

    @property
    def abspath(self):
        return os.path.join(settings.MEDIA_ROOT, release_download_path(self, self.filename))

    @property
    def relpath(self):
        return self.abspath[MEDIA_ROOT_LEN:]

    def absurl(self, request):
        return request.build_absolute_uri(settings.MEDIA_URL + release_download_path(self, self.filename))

    def globalurl(self):
        return settings.MEDIA_URL + release_download_path(self, self.filename)

    def data(self, request=None):
        result = dict([(x, getattr(self, x)) for x in ('has_sig', 'upload_time', 'comment_text', 'python_version',
                                                       'url', 'md5_digest', 'downloads', 'filename', 'size', )])
        if self.package_type:
            result['packagetype'] = self.package_type.name
        else:
            result['packagetype'] = None
        if request is not None:
            result['url'] = self.absurl(request)
        else:
            result['url'] = settings.MEDIA_URL + release_download_path(self, self.filename)
        return result


class Log(models.Model):
    package = models.ForeignKey(Package, db_index=True)
    release = models.ForeignKey(Release, db_index=True, blank=True, null=True)
    download = models.ForeignKey(ReleaseDownload, db_index=True, blank=True, null=True)
    timestamp = models.IntegerField(_('timestamp'))
    action = models.CharField(_('action'), max_length=455, blank=True, default='')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.timestamp = int(time.time())
        super(Log, self).save(force_insert=force_insert, force_update=force_update, using=using,
                              update_fields=update_fields)
