# -*- coding: utf-8 -*-
"""Here are defined Python functions of views.
Views are binded to URLs in :mod:`.urls`.
"""
import hashlib
import json
from json.encoder import JSONEncoder
import datetime
import mimetypes
import os
import stat
from django import forms
from django.conf import settings
from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse, Http404, QueryDict, StreamingHttpResponse, HttpResponseNotModified
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
import re
from django.views.static import was_modified_since
from pythonnest.models import Package, Release, ReleaseDownload, PackageRole, Classifier, Dependence, MEDIA_ROOT_LEN, \
    PackageType

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
    """Upload form"""
    search = forms.CharField(max_length=255)


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
    if action in ('submit', 'file_upload'):
        package_name = values.get('name', '')
        version_name = values.get('version', '')
        if not package_name or not version_name:
            raise PermissionDenied
        package, created = Package.objects.get_or_create(name=package_name)
        if not created:
            if PackageRole.objects.filter(package=package, user=request.user).count() == 0:
                raise PermissionDenied
        else:
            PackageRole(package=package, user=request.user, role=PackageRole.OWNER).save()
        for attr_name in ('name', 'home_page', 'author_email', 'download_url', 'author', 'license', 'summary',
                          'maintainer', 'maintainer_email', 'project_url'):
            if values.get(attr_name):
                setattr(package, attr_name, values.get(attr_name))
        package.save()
        release, created = Release.objects.get_or_create(package=package, version=version_name)
        for attr_name in ('stable_version', 'description', 'platform', 'keywords', 'docs_url',):
            if values.get(attr_name):
                setattr(package, attr_name, values.get(attr_name))
        release.classifiers.clear()
        for classifier in values.getlist('classifiers', []):
            release.classifiers.add(Classifier.get(classifier))
        for attr_name in ('requires', 'requires_dist', 'provides', 'provides_dist', 'obsoletes', 'obsoletes_dist',
                          'requires_external', 'requires_python'):
            getattr(release, attr_name).clear()
            for dep in values.getlist(attr_name, []):
                getattr(release, attr_name.add(Dependence.get(dep)))
        release.save()
    if action == 'file_upload':
        if 'content' not in files:
            raise PermissionDenied
        filename, content = files['content']
        #noinspection PyUnboundLocalVariable
        if ReleaseDownload.objects.filter(package=package, release=release, filename=filename).count() > 0:
            raise PermissionDenied
        md5 = hashlib.md5(content).hexdigest()
        if md5 != values.get('md5_digest'):
            raise PermissionDenied
        download = ReleaseDownload(package=package, release=release, filename=filename)
        path = download.abspath
        path_dirname = os.path.dirname(path)
        if not os.path.isdir(path_dirname):
            os.makedirs(path_dirname)
        with open(path, 'wb') as out_fd:
            out_fd.write(content)
        download.md5_digest = md5
        download.size = len(content)
        download.upload_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        download.url = settings.MEDIA_URL + path[MEDIA_ROOT_LEN:]
        download.file = download.relpath
        download.package_type = PackageType.get(values.get('filetype', 'source'))
        download.comment_text = values.get('comment', '')
        download.python_version = values.get('pyversion')
        download.log()
    template_values = {}
    return render_to_response('simple.html', template_values, RequestContext(request))


def static_serve(request, path, document_root=None):
    if document_root is None:
        document_root = settings.STATIC_ROOT
    filename = os.path.abspath(os.path.join(document_root, path))
    if not filename.startswith(document_root):
        raise Http404
    if settings.USE_XSENDFILE:
        return xsendfile(request, filename)
    return sendfile(request, filename)


def xsendfile(request, filename):
    response = HttpResponse()
    response['X-Sendfile'] = filename.encode('utf-8')
    return response


range_re = re.compile(r'bytes=(\d+)-(\d+)')


def sendfile(request, filename):
    # Respect the If-Modified-Since header.
    if not os.path.isfile(filename):
        raise Http404
    statobj = os.stat(filename)
    if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj[stat.ST_MTIME], statobj[stat.ST_SIZE]):
        return HttpResponseNotModified()
    content_type = mimetypes.guess_type(filename)[0]
    range_ = request.META.get('HTTP_RANGE', '')
    t = range_re.match(range_)
    size = os.path.getsize(filename)
    start = 0
    end = size - 1
    if t:
        start, end = int(t.group(1)), int(t.group(2))
    if end - start + 1 < size:
        obj = open(filename, 'rb')
        obj.seek(start)
        response = HttpResponse(obj.read(end - start + 1), content_type=content_type, status=206)
        response['Content-Range'] = 'bytes %d-%d/%d' % (start, end, size)
    else:
        obj = open(filename, 'rb')
        return StreamingHttpResponse(obj, content_type=content_type)
    response['Content-Length'] = end - start + 1
    #response["Last-Modified"] = http_date(statobj[stat.ST_MTIME])
    return response


def index(request):
    """Index view, displaying and processing a form."""
    search = SearchForm(request.GET)
    if search.is_valid():
        pattern = search.cleaned_data['search']
        if len(pattern) > 2:
            packages = Package.objects.filter(name__icontains=pattern).select_related()
        else:
            packages = Package.objects.filter(name__iexact=pattern).select_related()
        template_values = {'results': packages.distinct().select_related(), 'title': _('PythonNest')}
        return render_to_response('search_result.html', template_values, RequestContext(request))
    base_url = request.build_absolute_uri('/')
    template_values = {'base_url': base_url, }
    template_values.update(csrf(request))  # prevents cross-domain requests
    return render_to_response('index.html', template_values, RequestContext(request))


def show_package(request, package_id, release_id=None):
    package = get_object_or_404(Package, id=package_id)
    roles = PackageRole.objects.filter(package=package).select_related()
    releases = list(Release.objects.filter(package=package).order_by('-id').select_related())
    if release_id is None:
        release = releases[0] if releases else None
    else:
        release = get_object_or_404(Release, id=release_id, package=package)
    downloads = ReleaseDownload.objects.filter(release=release).order_by('filename')
    template_values = {'title': _('PythonNest — %(p)s') % {'p': package.name},
                       'package': package, 'roles': roles,
                       'is_editable': request.user in set([x.user for x in roles]),
                       'release': release, 'releases': releases, 'downloads': downloads,
                       }
    return render_to_response('show_package.html', template_values, RequestContext(request))
