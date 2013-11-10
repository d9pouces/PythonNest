from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rpc4django import rpcmethod
from pythonnest.models import Package, ReleaseDownload, Release, Log, PackageRole

__author__ = 'flanker'


@rpcmethod(signature=[])
def list_packages():
    """Retrieve a list of the package names registered with the package index. Returns a list of name strings."""
    return [x.name for x in Package.objects.all().only('name')]


@rpcmethod(signature=[str, bool])
def package_releases(package_name, show_hidden=False):
    """Retrieve a list of the releases registered for the given package_name. Returns a list with all version strings
    if show_hidden is True or only the non-hidden ones otherwise."""
    package = get_object_or_404(Package, name=package_name)
    query = package.release_set.all().only('version')
    if not show_hidden:
        query = query.filter(is_hidden=False)
    return [x.version for x in query]


@rpcmethod(signature=[str])
def package_roles(package_name):
    """Retrieve a list of users and their attributes roles for a given package_name. Role is either 'Maintainer' or
     'Owner'."""
    result = []
    for r in PackageRole.objects.filter(package__name=package_name).select_related('user'):
        result.append(('Maintainer' if r.role == PackageRole.MAINTAINER else 'Owner', r.user.username))
    return result


@rpcmethod(signature=[str])
def user_packages(user):
    """Retrieve a list of [role_name, package_name] for a given username. Role is either 'Maintainer' or 'Owner'."""
    user_obj = get_object_or_404(User, username=user)
    result = [('Owner', pkg.package.name, ) for pkg in PackageRole.objects.filter(user=user_obj).only('package__name')]
    result += [('Maintainer', pkg.package.name, ) for pkg in PackageRole.objects.filter(user=user_obj)
               .only('package__name')]
    return result


@rpcmethod(signature=[str, str])
def release_downloads(package_name, version):
    """Retrieve a list of files and download count for a given package and release version."""
    downloads = ReleaseDownload.objects.filter(package__name=package_name, release__version=version)
    return [(x.filename, x.downloads) for x in downloads.only('filename', 'downloads')]


@rpcmethod(signature=[str, str])
def release_urls(package_name, version):
    """Retrieve a list of download URLs for the given package release."""
    downloads = ReleaseDownload.objects.filter(package__name=package_name, release__version=version).select_related()
    return [download.data() for download in downloads]


@rpcmethod(signature=[str, str])
def release_data(package_name, version):
    """Retrieve metadata describing a specific package release. """
    releases = list(Release.objects.filter(package__name=package_name, version=version).select_related()[0:1])
    if not releases:
        return {}
    release = releases[0]
    return release.data()


@rpcmethod(signature=[int, bool])
def changelog(since, with_ids=False):
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


@rpcmethod(signature=[])
def changelog_last_serial():
    """Retrieve the last event's serial id."""
    return Log.objects.all().count()


@rpcmethod(signature=[int])
def changelog_since_serial(since_serial):
    """Retrieve a list of five-tuples (name, version, timestamp, action, serial) since the event identified by the
    given serial. All timestamps are UTC values. The argument is a UTC integer seconds since the epoch."""
    query = Log.objects.filter(id__gte=since_serial).order_by('id')
    result = [(x.package.name, x.release.version, x.timestamp, x.action, x.id) for x in query]
    return result


@rpcmethod(signature=[dict, str])
def search(spec, operator='and'):
    """Search the package database using the indicated search spec. """
    query = Release.objects.all().select_related()
    kwargs = {}
    for key in ('name', 'home_page', 'license', 'summary', 'download_url', 'author', 'author_email', 'maintainer',
                'maintainer_email'):
        if key not in spec:
            continue
        if isinstance(spec[key], list):
            if len(spec[key]) == 1:
                kwargs['package__' + key + '__icontains'] = spec[key][0]
            else:
                kwargs['package__' + key + '__in'] = spec[key]
        elif isinstance(spec[key], str):
            kwargs['package__' + key + '__icontains'] = spec[key]

    for key in ('version', 'description', 'keywords', 'platform'):
        if key not in spec:
            continue
        if isinstance(spec[key], list):
            if len(spec[key]) == 1:
                kwargs[key + '__icontains'] = spec[key][0]
            else:
                kwargs[key + '__in'] = spec[key]
        elif isinstance(spec[key], str):
            kwargs[key + '__icontains'] = spec[key]
    if operator == 'and':
        query = query.filter(**kwargs)
    else:
        subfilter = None
        for key, value in kwargs.items():
            if subfilter is None:
                subfilter = Q(**{key: value})
            else:
                subfilter |= Q(**{key: value})
        query = query.filter(subfilter)
    return [{'name': ans.name, 'version': ans.version, 'summary': ans.summary, '_pypi_ordering': 0} for ans in query]
