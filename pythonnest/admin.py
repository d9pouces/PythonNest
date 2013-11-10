# -*- coding: utf-8 -*-
"""Here are defined all admin models.
These admin models are associated to a :class:`django.db.models.Model`
and registered to the :class:`django.contrib.admin.site`.
"""
from django.contrib import admin
# from django.contrib import messages
# from django.utils.translation import ugettext_lazy as _
from pythonnest.models import PackageType, Package, Classifier, Dependence, ReleaseDownload, Release, \
    Synchronization, PackageRole

__author__ = "flanker"

#class SampleModelAdmin(admin.ModelAdmin):
#"""Extends the default admin views for SampleModel objects."""
#def remove_first_name(self, request, queryset):
#"""Remove first name of selected objects"""
#for obj in queryset:
#obj.first_name = ''
#obj.save()
#messages.info(request, _('First name removed'))
#remove_first_name.short_description = _('Remove first name')

#exclude = [] # list of fields to exclude
# # list of fields to display in the list
#list_display = ['family_name', 'first_name', 'birthday', ]
#list_filter = ['family_name', ] # list of filters to add on the sidebar
#   # fields to search against in the list
#search_fields = ['family_name', 'first_name', ]
#actions = [remove_first_name, ]
#admin.site.register(SampleModel, SampleModelAdmin)
admin.site.register(PackageType)
admin.site.register(Package)
admin.site.register(PackageRole)
admin.site.register(Classifier)
admin.site.register(Dependence)
admin.site.register(ReleaseDownload)
admin.site.register(Release)
admin.site.register(Synchronization)
