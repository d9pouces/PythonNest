# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Package.normalized_name'
        db.add_column('pythonnest_package', 'normalized_name',
                      self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, max_length=255, default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Package.normalized_name'
        db.delete_column('pythonnest_package', 'normalized_name')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pythonnest.classifier': {
            'Meta': {'object_name': 'Classifier'},
            'creation': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'})
        },
        'pythonnest.dependence': {
            'Meta': {'object_name': 'Dependence'},
            'creation': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'})
        },
        'pythonnest.log': {
            'Meta': {'object_name': 'Log'},
            'action': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"}),
            'download': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['pythonnest.ReleaseDownload']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pythonnest.Package']"}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['pythonnest.Release']"}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {})
        },
        'pythonnest.package': {
            'Meta': {'object_name': 'Package'},
            'author': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'author_email': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'download_url': ('django.db.models.fields.URLField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '200', 'default': "''"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['auth.Group']"}),
            'home_page': ('django.db.models.fields.URLField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '200', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'default': "'UNKNOWN'"}),
            'maintainer': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'maintainer_email': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'default': "''"}),
            'normalized_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'default': "''"}),
            'project_url': ('django.db.models.fields.URLField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '200', 'default': "''"}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"})
        },
        'pythonnest.packagerole': {
            'Meta': {'object_name': 'PackageRole'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pythonnest.Package']"}),
            'role': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'pythonnest.packagetype': {
            'Meta': {'object_name': 'PackageType'},
            'creation': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'})
        },
        'pythonnest.release': {
            'Meta': {'object_name': 'Release'},
            'classifiers': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'blank': 'True', 'null': 'True', 'symmetrical': 'False', 'to': "orm['pythonnest.Classifier']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True', 'default': "''"}),
            'docs_url': ('django.db.models.fields.URLField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '200', 'null': 'True', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'keywords': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'null': 'True', 'default': "''"}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now': 'True'}),
            'obsoletes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'related_name': "'dep_obsoletes'", 'to': "orm['pythonnest.Dependence']", 'db_index': 'True', 'symmetrical': 'False'}),
            'obsoletes_dist': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'related_name': "'dep_obsoletes_dist'", 'to': "orm['pythonnest.Dependence']", 'db_index': 'True', 'symmetrical': 'False'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pythonnest.Package']"}),
            'platform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '25', 'null': 'True', 'default': "'UNKNOWN'"}),
            'provides': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'related_name': "'dep_provides'", 'to': "orm['pythonnest.Dependence']", 'db_index': 'True', 'symmetrical': 'False'}),
            'provides_dist': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'related_name': "'dep_provides_dist'", 'to': "orm['pythonnest.Dependence']", 'db_index': 'True', 'symmetrical': 'False'}),
            'requires': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'related_name': "'dep_requires'", 'to': "orm['pythonnest.Dependence']", 'db_index': 'True', 'symmetrical': 'False'}),
            'requires_dist': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'related_name': "'dep_requires_dist'", 'to': "orm['pythonnest.Dependence']", 'db_index': 'True', 'symmetrical': 'False'}),
            'requires_external': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'related_name': "'dep_requires_external'", 'to': "orm['pythonnest.Dependence']", 'db_index': 'True', 'symmetrical': 'False'}),
            'requires_python': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'related_name': "'dep_requires_python'", 'to': "orm['pythonnest.Dependence']", 'db_index': 'True', 'symmetrical': 'False'}),
            'stable_version': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'null': 'True', 'default': "''"}),
            'version': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'null': 'True', 'default': "''"})
        },
        'pythonnest.releasedownload': {
            'Meta': {'object_name': 'ReleaseDownload'},
            'comment_text': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'downloads': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True', 'default': '0'}),
            'file': ('django.db.models.fields.files.FileField', [], {'db_index': 'True', 'max_length': '255'}),
            'filename': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'has_sig': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5_digest': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '40', 'default': "''"}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['pythonnest.Package']"}),
            'package_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['pythonnest.PackageType']", 'default': "'UNKNOWN'"}),
            'python_version': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'default': "'any'"}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pythonnest.Release']"}),
            'size': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True', 'default': '0'}),
            'uid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '40', 'default': "''"}),
            'upload_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'null': 'True', 'default': 'None'}),
            'url': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'default': "''"})
        },
        'pythonnest.releasemiss': {
            'Meta': {'object_name': 'ReleaseMiss'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pythonnest.Release']"})
        },
        'pythonnest.synchronization': {
            'Meta': {'object_name': 'Synchronization'},
            'creation': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'destination': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_serial': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True', 'default': 'None'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'default': "''"})
        }
    }

    complete_apps = ['pythonnest']