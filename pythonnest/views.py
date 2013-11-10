# -*- coding: utf-8 -*-
"""Here are defined Python functions of views.
Views are binded to URLs in :mod:`.urls`.
"""
import json
from json.encoder import JSONEncoder
import datetime
from django import forms
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
import django.contrib.admin.widgets
from pythonnest.models import Package, Release, ReleaseDownload

__author__ = "flanker"
# __copyright__ = "Copyright 2013, 19pouces.net"
# __credits__ = "flanker"
# __maintainer__ = "flanker"
# __email__ = "flanker@19pouces.net"

#from pythonnest import models


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
# def test(request, arg1, arg2):
    #"""Test view, displaying and processing a form."""
    #form = SampleForm()
    #template_values = {'arg1': arg1, 'arg2': arg2, }
    #template_values.update(csrf(request))  # prevents cross-domain requests
    #return render_to_response('test.html', template_values, RequestContext(request))


# easy_install