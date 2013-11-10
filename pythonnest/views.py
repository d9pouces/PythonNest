# -*- coding: utf-8 -*-
"""Here are defined Python functions of views.
Views are binded to URLs in :mod:`.urls`.
"""
import json
from json.encoder import JSONEncoder
import datetime
from django import forms
from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404, QueryDict
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from pythonnest.forms import RegisterForm
from pythonnest.models import Package, Release, ReleaseDownload, PackageRole

__author__ = "flanker"


class JSONDatetime(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%dT%H:%M:%S')
        return super(JSONDatetime, self).default(o)


def package_json(request, package_name):
    package = get_object_or_404(Package, name=package_name)
    releases = list(Release.objects.filter(package=package).order_by('-id')[0:1])
    if not releases:
        raise Http404
    release = releases[0]
    result = {'info': release.data(), 'urls': [x.data() for x in ReleaseDownload.objects.filter(release=release)]}
    return HttpResponse(json.dumps(result, ensure_ascii=False, cls=JSONDatetime, indent=4),
                        content_type='application/json')


def version_json(request, package_name, version):
    release = get_object_or_404(Release, package__name=package_name, version=version)
    result = {'info': release.data(), 'urls': [x.data() for x in ReleaseDownload.objects.filter(release=release)]}
    return HttpResponse(json.dumps(result, ensure_ascii=False, cls=JSONDatetime, indent=4),
                        content_type='application/json')


class SearchForm(forms.Form):
    """Sample form, with three fields."""
    # pylint: disable=R0903
    # pylint: disable=W0232
    search = forms.CharField(label=_('Pattern'), max_length=200, min_length=3,
                             widget=forms.widgets.TextInput(attrs={'placeholder': _('Please enter a word'), }))


def index(request):
    """Index view, displaying and processing a form."""
    results = []
    has_results = False
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():  # pylint: disable=E1101
            results = Package.objects.filter(name__icontains=form.cleaned_data['search']).select_related()
            has_results = True
    else:
        form = SearchForm()
    base_url = request.build_absolute_uri()
    template_values = {'form': form, 'results': results, 'has_results': has_results, 'base_url': base_url, }
    template_values.update(csrf(request))  # prevents cross-domain requests
    return render_to_response('index.html', template_values, RequestContext(request))


def simple(request, package_name=None, version=None):
    if package_name is not None:
        package = get_object_or_404(Package, name=package_name)
        if version is not None:
            version = get_object_or_404(Release, package=package, version=version)
            downloads = ReleaseDownload.objects.filter(version=version)
        else:
            downloads = ReleaseDownload.objects.filter(package=package)
    else:
        package = None
        downloads = ReleaseDownload.objects.all()
    template_values = {'package': package, 'downloads': downloads}
    return render_to_response('simple.html', template_values, RequestContext(request))


@csrf_exempt
def setup(request):
    if request.method != 'POST':
        raise PermissionDenied
    ct_type = request.META.get('CONTENT_TYPE', '')
    infos = [x.strip().partition('=') for x in ct_type.split(';')]
    boundary, encoding = None, 'ascii'
    for info in infos:
        if info[0] == 'boundary':
            boundary = info[2]
        elif info[0] == 'charset':
            encoding = info[2]
    if boundary is None:
        raise PermissionDenied
    mid_boundary = ('\n--' + boundary + '\n').encode(encoding)
    end_boundary = ('\n--' + boundary + '--\n').encode(encoding)
    fields = request.body.split(mid_boundary)
    values = QueryDict('', mutable=True, encoding=encoding)
    files = {}
    for part in fields:
        lines = part.split(b'\n\n', 1)
        if len(lines) != 2:
            continue
        infos = [x.strip().partition('=') for x in lines[0].decode(encoding).split(';')]
        key, filename = None, None
        for info in infos:
            if info[0] == 'name':
                key = info[2][1:-1]
            elif info[0] == 'filename':
                filename = info[2][1:-1]
        if key is None:
            continue
        value = lines[1]
        if value.endswith(end_boundary):
            value = value[:-len(end_boundary)]
        if filename is None:
            values.setlistdefault(key, [])
            values.appendlist(key, value)
        else:
            files[key] = filename, value
    action = values.get(':action')
    print(list(values.keys()))
    print(list(files.keys()))
    print(action)
    if action == 'submit':
        package, created = get_package(request, values.get('name', ''))
        for attr_name in ('name', 'home_page', 'author_email', 'download_url', 'author',  'license', 'summary',
                          'maintainer', 'maintainer_email', 'project_url'):
            if values.get(attr_name):
                setattr(package, attr_name, values.get(attr_name))
        package.save()
    elif action == 'file_upload':
        package, created = get_package(request, values.get('name', ''))
        for attr_name in ('name', 'home_page', 'author_email', 'download_url', 'author',  'license', 'summary',
                          'maintainer', 'maintainer_email', 'project_url'):
            if values.get(attr_name):
                setattr(package, attr_name, values.get(attr_name))
        package.save()
    a = ['license', 'home_page', 'name', 'filetype', 'comment', 'author', 'pyversion', 'summary', 'version',
         'protcol_version', ':action', 'metadata_version', 'md5_digest', 'download_url', 'platform', 'author_email',
         'classifiers', 'content"; filename="pythonnest-0.2.tar.gz']

    template_values = {}
    return render_to_response('simple.html', template_values, RequestContext(request))


def get_package(request, name):
    if not name:
        raise PermissionDenied
    obj, created = Package.objects.get_or_create(name=name)
    if not created:
        if PackageRole.objects.filter(package=obj, user=request.user).count() == 0:
            raise PermissionDenied
    else:
        PackageRole(package=obj, user=request.user, role=PackageRole.OWNER).save()
    return obj, created
