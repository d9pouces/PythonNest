# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import pythonnest.models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
        ('pythonnest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Classifier', max_length=255, db_index=True)),
                ('creation', models.DateTimeField(verbose_name='creation', auto_now_add=True, db_index=True)),
                ('modification', models.DateTimeField(verbose_name='modification', auto_now=True, db_index=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dependence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Classifier', max_length=255, db_index=True)),
                ('creation', models.DateTimeField(verbose_name='creation', auto_now_add=True, db_index=True)),
                ('modification', models.DateTimeField(verbose_name='modification', auto_now=True, db_index=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('timestamp', models.IntegerField(verbose_name='timestamp')),
                ('action', models.CharField(blank=True, verbose_name='action', max_length=255, default='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name',
                 models.CharField(blank=True, verbose_name='package name', max_length=255, default='', db_index=True)),
                ('normalized_name',
                 models.CharField(blank=True, verbose_name='normalized name', max_length=255, default='',
                                  db_index=True)),
                ('author',
                 models.CharField(blank=True, verbose_name='author', max_length=255, db_index=True, null=True)),
                ('author_email',
                 models.CharField(blank=True, verbose_name='author email', max_length=255, db_index=True, null=True)),
                ('maintainer',
                 models.CharField(blank=True, verbose_name='maintainer', max_length=255, db_index=True, null=True)),
                ('maintainer_email',
                 models.CharField(blank=True, verbose_name='maintainer email', max_length=255, db_index=True,
                                  null=True)),
                ('home_page', models.URLField(blank=True, verbose_name='home page', default='', db_index=True)),
                ('license', models.CharField(blank=True, verbose_name='license', max_length=255, default='UNKNOWN',
                                             db_index=True)),
                ('summary', models.TextField(blank=True, verbose_name='summary', default='')),
                ('download_url', models.URLField(blank=True, verbose_name='download url', default='', db_index=True)),
                ('project_url', models.URLField(blank=True, verbose_name='project url', default='', db_index=True)),
                ('creation', models.DateTimeField(verbose_name='creation', auto_now_add=True, db_index=True)),
                ('modification', models.DateTimeField(verbose_name='modification', auto_now=True, db_index=True)),
                ('group',
                 models.ForeignKey(blank=True, verbose_name='restrict to this group', null=True, to='auth.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PackageRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('role', models.IntegerField(verbose_name='role', default=1, choices=[(1, 'owner'), (2, 'maintainer')],
                                             db_index=True)),
                ('package', models.ForeignKey(to='pythonnest.Package', verbose_name='package')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PackageType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Classifier', max_length=255, db_index=True)),
                ('creation', models.DateTimeField(verbose_name='creation', auto_now_add=True, db_index=True)),
                ('modification', models.DateTimeField(verbose_name='modification', auto_now=True, db_index=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('version',
                 models.CharField(blank=True, verbose_name='version name', null=True, max_length=255, default='',
                                  db_index=True)),
                ('stable_version',
                 models.CharField(blank=True, verbose_name='stable version name', null=True, max_length=255, default='',
                                  db_index=True)),
                ('description', models.TextField(blank=True, verbose_name='Description', default='', null=True)),
                ('platform',
                 models.CharField(blank=True, verbose_name='platform', null=True, max_length=25, default='UNKNOWN',
                                  db_index=True)),
                ('keywords',
                 models.CharField(blank=True, verbose_name='keywords', null=True, max_length=255, default='',
                                  db_index=True)),
                (
                    'docs_url', models.URLField(blank=True, verbose_name='docs url', null=True, default='',
                                                db_index=True)),
                ('creation', models.DateTimeField(verbose_name='creation', auto_now_add=True, db_index=True)),
                ('modification', models.DateTimeField(verbose_name='modification', auto_now=True, db_index=True)),
                ('is_hidden', models.BooleanField(verbose_name='Is hidden', default=False, db_index=True)),
                ('classifiers',
                 models.ManyToManyField(blank=True, to='pythonnest.Classifier', db_index=True, null=True)),
                ('obsoletes',
                 models.ManyToManyField(blank=True, to='pythonnest.Dependence', related_name='dep_obsoletes',
                                        db_index=True, null=True)),
                ('obsoletes_dist',
                 models.ManyToManyField(blank=True, to='pythonnest.Dependence', related_name='dep_obsoletes_dist',
                                        db_index=True, null=True)),
                ('package', models.ForeignKey(to='pythonnest.Package')),
                ('provides', models.ManyToManyField(blank=True, to='pythonnest.Dependence', related_name='dep_provides',
                                                    db_index=True, null=True)),
                ('provides_dist',
                 models.ManyToManyField(blank=True, to='pythonnest.Dependence', related_name='dep_provides_dist',
                                        db_index=True, null=True)),
                ('requires', models.ManyToManyField(blank=True, to='pythonnest.Dependence', related_name='dep_requires',
                                                    db_index=True, null=True)),
                ('requires_dist',
                 models.ManyToManyField(blank=True, to='pythonnest.Dependence', related_name='dep_requires_dist',
                                        db_index=True, null=True)),
                ('requires_external',
                 models.ManyToManyField(blank=True, to='pythonnest.Dependence', related_name='dep_requires_external',
                                        db_index=True, null=True)),
                ('requires_python',
                 models.ManyToManyField(blank=True, to='pythonnest.Dependence', related_name='dep_requires_python',
                                        db_index=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReleaseDownload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('uid', models.CharField(blank=True, verbose_name='UID', max_length=40, default='', db_index=True)),
                ('url', models.CharField(blank=True, verbose_name='URL', max_length=255, default='', db_index=True)),
                ('filename', models.CharField(verbose_name='Filename', max_length=255, db_index=True)),
                ('file', models.FileField(verbose_name='File', max_length=255,
                                          upload_to=pythonnest.models.release_download_path, db_index=True)),
                ('size', models.IntegerField(blank=True, verbose_name='Size', default=0, db_index=True)),
                ('md5_digest',
                 models.CharField(blank=True, verbose_name='MD5', max_length=40, default='', db_index=True)),
                ('downloads', models.IntegerField(blank=True, verbose_name='Downloads', default=0, db_index=True)),
                ('has_sig', models.BooleanField(verbose_name='Has signature', default=False, db_index=True)),
                ('python_version',
                 models.CharField(blank=True, verbose_name='Python version', max_length=255, default='any',
                                  db_index=True)),
                ('comment_text', models.TextField(blank=True, verbose_name='Comment', default='')),
                ('upload_time',
                 models.DateTimeField(blank=True, verbose_name='Upload time', default=None, db_index=True, null=True)),
                ('creation', models.DateTimeField(verbose_name='creation', auto_now_add=True, db_index=True)),
                ('modification', models.DateTimeField(verbose_name='modification', auto_now=True, db_index=True)),
                ('package', models.ForeignKey(blank=True, null=True, to='pythonnest.Package')),
                ('package_type', models.ForeignKey(blank=True, null=True, to='pythonnest.PackageType', default=None)),
                ('release', models.ForeignKey(to='pythonnest.Release')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReleaseMiss',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('release', models.ForeignKey(to='pythonnest.Release')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Synchronization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('source',
                 models.CharField(blank=True, verbose_name='Source', max_length=255, default='', db_index=True)),
                ('destination',
                 models.CharField(blank=True, verbose_name='Destination', max_length=255, default='', db_index=True)),
                ('last_serial',
                 models.IntegerField(blank=True, verbose_name='Last synchronized serial', default=None, null=True)),
                ('creation', models.DateTimeField(verbose_name='creation', auto_now_add=True, db_index=True)),
                ('modification', models.DateTimeField(verbose_name='modification', auto_now=True, db_index=True)),
            ],
            options={
                'verbose_name': 'Synchronization',
                'verbose_name_plural': 'Synchronizations',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='log',
            name='download',
            field=models.ForeignKey(blank=True, null=True, to='pythonnest.ReleaseDownload'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='log',
            name='package',
            field=models.ForeignKey(to='pythonnest.Package'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='log',
            name='release',
            field=models.ForeignKey(blank=True, null=True, to='pythonnest.Release'),
            preserve_default=True,
        ),
    ]
