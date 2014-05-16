# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Synchronization'
        db.create_table('pythonnest_synchronization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, max_length=255, default='')),
            ('destination', self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, max_length=255, default='')),
            ('last_serial', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True, default=None)),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now_add=True)),
            ('modification', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now=True)),
        ))
        db.send_create_signal('pythonnest', ['Synchronization'])

        # Adding model 'Classifier'
        db.create_table('pythonnest_classifier', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255)),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now_add=True)),
            ('modification', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now=True)),
        ))
        db.send_create_signal('pythonnest', ['Classifier'])

        # Adding model 'Dependence'
        db.create_table('pythonnest_dependence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255)),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now_add=True)),
            ('modification', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now=True)),
        ))
        db.send_create_signal('pythonnest', ['Dependence'])

        # Adding model 'PackageType'
        db.create_table('pythonnest_packagetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255)),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now_add=True)),
            ('modification', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now=True)),
        ))
        db.send_create_signal('pythonnest', ['PackageType'])

        # Adding model 'Package'
        db.create_table('pythonnest_package', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, max_length=255, default='')),
            ('author', self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, null=True, max_length=255)),
            ('author_email', self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, null=True, max_length=255)),
            ('maintainer', self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, null=True, max_length=255)),
            ('maintainer_email', self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, null=True, max_length=255)),
            ('home_page', self.gf('django.db.models.fields.URLField')(db_index=True, blank=True, max_length=200, default='')),
            ('license', self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, max_length=255, default='UNKNOWN')),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True, default='')),
            ('download_url', self.gf('django.db.models.fields.URLField')(db_index=True, blank=True, max_length=200, default='')),
            ('project_url', self.gf('django.db.models.fields.URLField')(db_index=True, blank=True, max_length=200, default='')),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now_add=True)),
            ('modification', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['auth.Group'])),
        ))
        db.send_create_signal('pythonnest', ['Package'])

        # Adding model 'PackageRole'
        db.create_table('pythonnest_packagerole', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('role', self.gf('django.db.models.fields.IntegerField')(db_index=True, default=1)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pythonnest.Package'])),
        ))
        db.send_create_signal('pythonnest', ['PackageRole'])

        # Adding model 'Release'
        db.create_table('pythonnest_release', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pythonnest.Package'])),
            ('version', self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, max_length=255, null=True, default='')),
            ('stable_version', self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, max_length=255, null=True, default='')),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True, null=True, default='')),
            ('platform', self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, max_length=25, null=True, default='UNKNOWN')),
            ('keywords', self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, max_length=255, null=True, default='')),
            ('docs_url', self.gf('django.db.models.fields.URLField')(db_index=True, blank=True, max_length=200, null=True, default='')),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now_add=True)),
            ('modification', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now=True)),
            ('is_hidden', self.gf('django.db.models.fields.BooleanField')(db_index=True, default=False)),
        ))
        db.send_create_signal('pythonnest', ['Release'])

        # Adding M2M table for field classifiers on 'Release'
        m2m_table_name = db.shorten_name('pythonnest_release_classifiers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('release', models.ForeignKey(orm['pythonnest.release'], null=False)),
            ('classifier', models.ForeignKey(orm['pythonnest.classifier'], null=False))
        ))
        db.create_unique(m2m_table_name, ['release_id', 'classifier_id'])

        # Adding M2M table for field requires on 'Release'
        m2m_table_name = db.shorten_name('pythonnest_release_requires')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('release', models.ForeignKey(orm['pythonnest.release'], null=False)),
            ('dependence', models.ForeignKey(orm['pythonnest.dependence'], null=False))
        ))
        db.create_unique(m2m_table_name, ['release_id', 'dependence_id'])

        # Adding M2M table for field requires_dist on 'Release'
        m2m_table_name = db.shorten_name('pythonnest_release_requires_dist')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('release', models.ForeignKey(orm['pythonnest.release'], null=False)),
            ('dependence', models.ForeignKey(orm['pythonnest.dependence'], null=False))
        ))
        db.create_unique(m2m_table_name, ['release_id', 'dependence_id'])

        # Adding M2M table for field provides on 'Release'
        m2m_table_name = db.shorten_name('pythonnest_release_provides')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('release', models.ForeignKey(orm['pythonnest.release'], null=False)),
            ('dependence', models.ForeignKey(orm['pythonnest.dependence'], null=False))
        ))
        db.create_unique(m2m_table_name, ['release_id', 'dependence_id'])

        # Adding M2M table for field provides_dist on 'Release'
        m2m_table_name = db.shorten_name('pythonnest_release_provides_dist')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('release', models.ForeignKey(orm['pythonnest.release'], null=False)),
            ('dependence', models.ForeignKey(orm['pythonnest.dependence'], null=False))
        ))
        db.create_unique(m2m_table_name, ['release_id', 'dependence_id'])

        # Adding M2M table for field obsoletes on 'Release'
        m2m_table_name = db.shorten_name('pythonnest_release_obsoletes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('release', models.ForeignKey(orm['pythonnest.release'], null=False)),
            ('dependence', models.ForeignKey(orm['pythonnest.dependence'], null=False))
        ))
        db.create_unique(m2m_table_name, ['release_id', 'dependence_id'])

        # Adding M2M table for field obsoletes_dist on 'Release'
        m2m_table_name = db.shorten_name('pythonnest_release_obsoletes_dist')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('release', models.ForeignKey(orm['pythonnest.release'], null=False)),
            ('dependence', models.ForeignKey(orm['pythonnest.dependence'], null=False))
        ))
        db.create_unique(m2m_table_name, ['release_id', 'dependence_id'])

        # Adding M2M table for field requires_external on 'Release'
        m2m_table_name = db.shorten_name('pythonnest_release_requires_external')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('release', models.ForeignKey(orm['pythonnest.release'], null=False)),
            ('dependence', models.ForeignKey(orm['pythonnest.dependence'], null=False))
        ))
        db.create_unique(m2m_table_name, ['release_id', 'dependence_id'])

        # Adding M2M table for field requires_python on 'Release'
        m2m_table_name = db.shorten_name('pythonnest_release_requires_python')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('release', models.ForeignKey(orm['pythonnest.release'], null=False)),
            ('dependence', models.ForeignKey(orm['pythonnest.dependence'], null=False))
        ))
        db.create_unique(m2m_table_name, ['release_id', 'dependence_id'])

        # Adding model 'ReleaseMiss'
        db.create_table('pythonnest_releasemiss', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('release', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pythonnest.Release'])),
        ))
        db.send_create_signal('pythonnest', ['ReleaseMiss'])

        # Adding model 'ReleaseDownload'
        db.create_table('pythonnest_releasedownload', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['pythonnest.Package'])),
            ('release', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pythonnest.Release'])),
            ('uid', self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, max_length=40, default='')),
            ('url', self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, max_length=255, default='')),
            ('package_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['pythonnest.PackageType'], default='UNKNOWN')),
            ('filename', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255)),
            ('file', self.gf('django.db.models.fields.files.FileField')(db_index=True, max_length=255)),
            ('size', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True, default=0)),
            ('md5_digest', self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, max_length=40, default='')),
            ('downloads', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True, default=0)),
            ('has_sig', self.gf('django.db.models.fields.BooleanField')(db_index=True, default=False)),
            ('python_version', self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, max_length=255, default='any')),
            ('comment_text', self.gf('django.db.models.fields.TextField')(blank=True, default='')),
            ('upload_time', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, null=True, default=None)),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now_add=True)),
            ('modification', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now=True)),
        ))
        db.send_create_signal('pythonnest', ['ReleaseDownload'])

        # Adding model 'Log'
        db.create_table('pythonnest_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pythonnest.Package'])),
            ('release', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['pythonnest.Release'])),
            ('download', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['pythonnest.ReleaseDownload'])),
            ('timestamp', self.gf('django.db.models.fields.IntegerField')()),
            ('action', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255, default='')),
        ))
        db.send_create_signal('pythonnest', ['Log'])


    def backwards(self, orm):
        # Deleting model 'Synchronization'
        db.delete_table('pythonnest_synchronization')

        # Deleting model 'Classifier'
        db.delete_table('pythonnest_classifier')

        # Deleting model 'Dependence'
        db.delete_table('pythonnest_dependence')

        # Deleting model 'PackageType'
        db.delete_table('pythonnest_packagetype')

        # Deleting model 'Package'
        db.delete_table('pythonnest_package')

        # Deleting model 'PackageRole'
        db.delete_table('pythonnest_packagerole')

        # Deleting model 'Release'
        db.delete_table('pythonnest_release')

        # Removing M2M table for field classifiers on 'Release'
        db.delete_table(db.shorten_name('pythonnest_release_classifiers'))

        # Removing M2M table for field requires on 'Release'
        db.delete_table(db.shorten_name('pythonnest_release_requires'))

        # Removing M2M table for field requires_dist on 'Release'
        db.delete_table(db.shorten_name('pythonnest_release_requires_dist'))

        # Removing M2M table for field provides on 'Release'
        db.delete_table(db.shorten_name('pythonnest_release_provides'))

        # Removing M2M table for field provides_dist on 'Release'
        db.delete_table(db.shorten_name('pythonnest_release_provides_dist'))

        # Removing M2M table for field obsoletes on 'Release'
        db.delete_table(db.shorten_name('pythonnest_release_obsoletes'))

        # Removing M2M table for field obsoletes_dist on 'Release'
        db.delete_table(db.shorten_name('pythonnest_release_obsoletes_dist'))

        # Removing M2M table for field requires_external on 'Release'
        db.delete_table(db.shorten_name('pythonnest_release_requires_external'))

        # Removing M2M table for field requires_python on 'Release'
        db.delete_table(db.shorten_name('pythonnest_release_requires_python'))

        # Deleting model 'ReleaseMiss'
        db.delete_table('pythonnest_releasemiss')

        # Deleting model 'ReleaseDownload'
        db.delete_table('pythonnest_releasedownload')

        # Deleting model 'Log'
        db.delete_table('pythonnest_log')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'}),
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
            'author': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'null': 'True', 'max_length': '255'}),
            'author_email': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'null': 'True', 'max_length': '255'}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'download_url': ('django.db.models.fields.URLField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '200', 'default': "''"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['auth.Group']"}),
            'home_page': ('django.db.models.fields.URLField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '200', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'default': "'UNKNOWN'"}),
            'maintainer': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'null': 'True', 'max_length': '255'}),
            'maintainer_email': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'null': 'True', 'max_length': '255'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'default': "''"}),
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
            'classifiers': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'blank': 'True', 'null': 'True', 'to': "orm['pythonnest.Classifier']", 'symmetrical': 'False'}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True', 'default': "''"}),
            'docs_url': ('django.db.models.fields.URLField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '200', 'null': 'True', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'keywords': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'null': 'True', 'default': "''"}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now': 'True'}),
            'obsoletes': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'null': 'True', 'to': "orm['pythonnest.Dependence']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'dep_obsoletes'"}),
            'obsoletes_dist': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'null': 'True', 'to': "orm['pythonnest.Dependence']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'dep_obsoletes_dist'"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pythonnest.Package']"}),
            'platform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '25', 'null': 'True', 'default': "'UNKNOWN'"}),
            'provides': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'null': 'True', 'to': "orm['pythonnest.Dependence']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'dep_provides'"}),
            'provides_dist': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'null': 'True', 'to': "orm['pythonnest.Dependence']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'dep_provides_dist'"}),
            'requires': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'null': 'True', 'to': "orm['pythonnest.Dependence']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'dep_requires'"}),
            'requires_dist': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'null': 'True', 'to': "orm['pythonnest.Dependence']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'dep_requires_dist'"}),
            'requires_external': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'null': 'True', 'to': "orm['pythonnest.Dependence']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'dep_requires_external'"}),
            'requires_python': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'null': 'True', 'to': "orm['pythonnest.Dependence']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'dep_requires_python'"}),
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