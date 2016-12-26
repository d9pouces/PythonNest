# -*- coding: utf-8 -*-
"""
This file describes REST API, built on top of django-tastypie.
"""
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from pythonnest.models import Package, PackageRole, ReleaseDownload, Release, Log
from pythonnest.views import prepare_query
from pythonnest.xmlrpc import register_rpc_method


__author__ = 'Matthieu Gallet'


# noinspection PyUnusedLocal
@register_rpc_method
def list_packages(request):
    """Retrieve a list of the package names registered with the package index. Returns a list of name strings."""
    return [x.name for x in Package.objects.all().only('name')]


# noinspection PyUnusedLocal
@register_rpc_method
def package_releases(request, package_name: str, show_hidden: bool=False):
    """Retrieve a list of the releases registered for the given package_name. Returns a list with all version strings
    if show_hidden is True or only the non-hidden ones otherwise."""
    package = get_object_or_404(Package, name=package_name)
    query = package.release_set.all().only('version')
    if not show_hidden:
        query = query.filter(is_hidden=False)
    return [x.version for x in query]


# noinspection PyUnusedLocal
@register_rpc_method
def package_roles(request, package_name: str):
    """Retrieve a list of users and their attributes roles for a given package_name. Role is either 'Maintainer' or
     'Owner'."""
    result = []
    for r in PackageRole.objects.filter(package__name=package_name).select_related('user'):
        result.append(('Maintainer' if r.role == PackageRole.MAINTAINER else 'Owner', r.user.username))
    return result


# noinspection PyUnusedLocal
@register_rpc_method
def user_packages(request, user: str):
    """Retrieve a list of [role_name, package_name] for a given username. Role is either 'Maintainer' or 'Owner'."""
    user_obj = get_object_or_404(User, username=user)
    result = [('Owner', pkg.package.name, ) for pkg in PackageRole.objects.filter(user=user_obj).only('package__name')]
    result += [('Maintainer', pkg.package.name, ) for pkg in PackageRole.objects.filter(user=user_obj)
               .only('package__name')]
    return result


# noinspection PyUnusedLocal
@register_rpc_method
def release_downloads(request, package_name: str, version: str):
    """Retrieve a list of files and download count for a given package and release version."""
    downloads = ReleaseDownload.objects.filter(package__name=package_name, release__version=version)
    return [(x.filename, x.downloads) for x in downloads.only('filename', 'downloads')]


# noinspection PyUnusedLocal
@register_rpc_method
def release_urls(request, package_name: str, version: str):
    """Retrieve a list of download URLs for the given package release."""
    downloads = ReleaseDownload.objects.filter(package__name=package_name, release__version=version).select_related()
    return [download.data() for download in downloads]


# noinspection PyUnusedLocal
@register_rpc_method
def release_data(request, package_name: str, version: str):
    """Retrieve metadata describing a specific package release. """
    releases = list(Release.objects.filter(package__name=package_name, version=version).select_related()[0:1])
    if not releases:
        return {}
    release = releases[0]
    return release.data()


# noinspection PyUnusedLocal
@register_rpc_method
def changelog(request, since: int, with_ids: bool=False):
    """Retrieve a list of four-tuples (name, version, timestamp, action), or five-tuple including the serial id if ids
    are requested, since the given timestamp. All timestamps are UTC values. The argument is a UTC integer seconds
    since the epoch.
    """
    query = Log.objects.filter(timestamp__gte=since).order_by('id')
    if with_ids:
        result = [(x.package.name, x.release.version, x.timestamp, x.action, x.id) for x in query]
    else:
        result = [(x.package.name, x.release.version, x.timestamp, x.action) for x in query]
    return result


# noinspection PyUnusedLocal
@register_rpc_method
def changelog_last_serial(request):
    """Retrieve the last event's serial id."""
    return Log.objects.all().count()


# noinspection PyUnusedLocal
@register_rpc_method
def changelog_since_serial(request, since_serial: int):
    """Retrieve a list of five-tuples (name, version, timestamp, action, serial) since the event identified by the
    given serial. All timestamps are UTC values. The argument is a UTC integer seconds since the epoch."""
    query = Log.objects.filter(id__gte=since_serial).order_by('id')
    result = [(x.package.name, x.release.version, x.timestamp, x.action, x.id) for x in query]
    return result


# noinspection PyUnusedLocal
@register_rpc_method
def search(request, spec, operator: str='and'):
    """Search the package database using the indicated search spec. """
    sub_query = None
    for key in ('name', 'home_page', 'license', 'summary', 'download_url', 'author', 'author_email', 'maintainer',
                'maintainer_email'):
        if key not in spec:
            continue
        sub_query = prepare_query(sub_query, 'package__', key, spec[key], global_and=(operator == 'and'))
    for key in ('version', 'description', 'keywords', 'platform'):
        if key not in spec:
            continue
        sub_query = prepare_query(sub_query, '', key, spec[key], global_and=(operator == 'and'))
    query = Release.objects.filter(sub_query).select_related()
    return [{'name': ans.name, 'version': ans.version, 'summary': ans.summary, '_pypi_ordering': 0} for ans in query]
