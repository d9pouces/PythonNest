# -*- coding: utf-8 -*-
"""Here are defined Python functions of views.
Views are binded to URLs in :mod:`.urls`.
"""
from distutils.version import LooseVersion
import hashlib
import json
from json.encoder import JSONEncoder
import datetime
import mimetypes
import os
import stat
import re
import math

from django import forms
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, QueryDict, StreamingHttpResponse, HttpResponseNotModified, \
    HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect, resolve_url
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _, ugettext
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.views.static import was_modified_since

from pythonnest.models import Package, Release, ReleaseDownload, PackageRole, Classifier, Dependence, MEDIA_ROOT_LEN, \
    PackageType
from pythonnest.rpcapi.utils import prepare_query


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
        package = get_object_or_404(Package, name__iexact=package_name)
        if version is not None:
            release = get_object_or_404(Release, package=package, version__iexact=version)
            downloads = ReleaseDownload.objects.filter(release=release)
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
        raise PermissionDenied(_('Only POST request are allowed'))
    ct_type = request.META.get('CONTENT_TYPE', '')
    infos = [x.strip().partition('=') for x in ct_type.split(';')]
    boundary, encoding = None, 'ascii'
    for info in infos:
        if info[0] == 'boundary':
            boundary = info[2]
        elif info[0] == 'charset':
            encoding = info[2]
    if boundary is None:
        raise PermissionDenied(_('Invalid POST form'))
        # parse the POST query by hand
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
        # the POST data are parsed, let's go
    action = values.get(':action')
    if action in ('submit', 'file_upload'):
        package_name = values.get('name', '')
        version_name = values.get('version', '')
        if not package_name or not version_name:
            raise PermissionDenied(_('No package name provided'))
        if request.user.is_anonymous():
            return HttpResponse(ugettext('You must be authenticated'), status=401)
        package, package_created = Package.objects.get_or_create(name=package_name)
        if package_created:
            PackageRole(package=package, user=request.user, role=PackageRole.OWNER).save()
        elif not request.user.is_superuser:
            if PackageRole.objects.filter(package=package, user=request.user).count() == 0:
                return HttpResponse(ugettext('You are not allowed to update this package'), status=401)
        for attr_name in ('name', 'home_page', 'author_email', 'download_url', 'author', 'license', 'summary',
                          'maintainer', 'maintainer_email', 'project_url', ):
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
                getattr(release, attr_name).add(Dependence.get(dep))
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


def index(request, page='0', size='20'):
    """Index view, displaying and processing a form."""
    search = SearchForm(request.GET)
    if search.is_valid():
        orig_pattern = search.cleaned_data['search']
        alt_pattern = None if orig_pattern.find('*') > -1 else ('*%s*' % orig_pattern)
        alt_url = reverse('pythonnest.views.index')

        patterns = orig_pattern.split()
        sub_query = None
        for pattern in patterns:
            sub_query = prepare_query(sub_query, '', 'name', pattern, global_and=True)
        query = Package.objects.filter(sub_query).distinct()
        page_int = int(page)
        page_size = int(size)
        packages = list(query.select_related()[page_int * page_size:(page_int + 1) * page_size])
        total = query.count()
        page_count = math.ceil(total / page_size)
        page_index = page_int + 1
        template_values = {'results': packages, 'title': _('PythonNest'), 'alt_pattern': alt_pattern,
                           'page_count': page_count, 'page_index': page_index, 'alt_url': alt_url,
                           'previous_page': None if page_int <= 0 else page_int - 1, 'pattern': orig_pattern,
                           'next_page': None if page_index >= page_count else page_index, }
        return render_to_response('search_result.html', template_values, RequestContext(request))
    base_url = settings.HOST
    use_ssl = base_url.startswith('https://')
    template_values = {'base_url': base_url, 'use_ssl': use_ssl, }
    template_values.update(csrf(request))  # prevents cross-domain requests
    return render_to_response('index.html', template_values, RequestContext(request))


def show_package(request, package_id, release_id=None):
    package = get_object_or_404(Package, id=package_id)
    roles = PackageRole.objects.filter(package=package).order_by('role').select_related()
    releases = list(Release.objects.filter(package=package).order_by('-id').select_related())
    release = None
    releases = sorted(releases, key=lambda x: LooseVersion(str(x.version)), reverse=True)
    if release_id is not None:
        release = get_object_or_404(Release, id=release_id, package=package)
    elif releases:
        release = releases[0]

    class RoleForm(forms.Form):
        username = forms.CharField(max_length=255, label=_('Username'))
        role = forms.ChoiceField(required=False, widget=forms.Select(), choices=PackageRole.ROLES, label=_('Role'))

    downloads = ReleaseDownload.objects.filter(release=release).order_by('filename')
    is_admin = package.is_admin(request.user)
    add_user_form = None
    if is_admin:
        if request.method == 'POST':
            add_user_form = RoleForm(request.POST)
            if add_user_form.is_valid():
                username = add_user_form.cleaned_data['username']
                role = add_user_form.cleaned_data['role']
                user = User.objects.get_or_create(username=username)[0]
                PackageRole.objects.get_or_create(package=package, user=user, role=int(role))
                return redirect('pythonnest.views.show_package', package_id=package_id)
        else:
            add_user_form = RoleForm()
    template_values = {'title': _('PythonNest'),
                       'package': package, 'roles': roles, 'is_admin': is_admin, 'add_user_form': add_user_form,
                       'is_editable': request.user in set([x.user for x in roles]),
                       'release': release, 'releases': releases, 'downloads': downloads, }
    template_values.update(csrf(request))
    return render_to_response('show_package.html', template_values, RequestContext(request))


@login_required
def delete_download(request, download_id):
    download = get_object_or_404(ReleaseDownload, id=download_id)
    package = download.package
    release = download.release
    if PackageRole.objects.filter(package=package, role=PackageRole.OWNER, user=request.user).count() == 0 and \
            not request.user.is_superuser:
        raise PermissionDenied
    abspath = download.abspath
    download.delete()
    if os.path.isfile(abspath):
        os.remove(abspath)
    if ReleaseDownload.objects.filter(release=release).count() == 0:
        release.delete()
        response = HttpResponseRedirect(reverse('pythonnest.views.show_package', kwargs={'package_id': package.id}))
    else:
        response = HttpResponseRedirect(reverse('pythonnest.views.show_package',
                                                kwargs={'package_id': package.id, 'release_id': release.id}))
    if Release.objects.filter(package=package).count() == 0:
        package.delete()
        response = HttpResponseRedirect(reverse('pythonnest.views.index'))
    return response


@login_required
def delete_role(request, role_id):
    role = get_object_or_404(PackageRole, id=role_id)
    package = role.package
    if not package.is_admin(request.user):
        raise PermissionDenied
    role.delete()
    return redirect('pythonnest.views.show_package', package_id=package.id)


def show_classifier(request, classifier_id, page='0', size='20'):
    classifier = get_object_or_404(Classifier, id=classifier_id)
    page_int = int(page)
    page_size = int(size)
    releases = list(classifier.release_set.all().select_related('package')
                    .order_by('-id')[page_int * page_size:(page_int + 1) * page_size])
    total = classifier.release_set.all().count()
    page_count = math.ceil(total / page_size)
    page_index = page_int + 1
    template_values = {'title': _('PythonNest - %(c)s') % {'c': classifier.name},
                       'releases': releases, 'page_count': page_count, 'page_index': page_index,
                       'previous_page': None if page_int <= 0 else page_int - 1, 'classifier': classifier,
                       'next_page': None if page_index >= page_count else page_index, }
    return render_to_response('classifier.html', template_values, RequestContext(request))


@sensitive_post_parameters()
@never_cache
def create_user(request, template_name='create_user.html',
                redirect_field_name=REDIRECT_FIELD_NAME,
                user_creation_form=UserCreationForm,
                current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = user_creation_form(data=request.POST)
        if form.is_valid():
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            form.save(commit=True)
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(redirect_to)
    else:
        form = user_creation_form()
    request.session.set_test_cookie()
    current_site = get_current_site(request)
    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context, current_app=current_app)