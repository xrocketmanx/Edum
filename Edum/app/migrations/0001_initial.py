# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('answer', models.TextField()),
                ('correct', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=250)),
                ('overview', models.TextField()),
                ('duration', models.IntegerField()),
                ('author', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseProgress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('progress', models.IntegerField(default=0)),
                ('course', models.ForeignKey(to='app.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('video_url', models.TextField()),
                ('name', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('test_count', models.IntegerField(default=0)),
                ('lecture_count', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=250)),
                ('overview', models.TextField()),
                ('course', models.ForeignKey(to='app.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('answer_count', models.IntegerField()),
                ('question', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('question_count', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=250)),
                ('duration', models.IntegerField()),
                ('module', models.ForeignKey(to='app.Module')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('passed', models.BooleanField(default=False)),
                ('test', models.ForeignKey(to='app.Test')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('first_name', models.CharField(max_length=40)),
                ('second_name', models.CharField(max_length=40)),
                ('login', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=16)),
                ('courses_results', models.ManyToManyField(to='app.Course', through='app.CourseProgress')),
                ('signed_courses', models.ManyToManyField(related_name='signed_courses', to='app.Course')),
                ('tests_results', models.ManyToManyField(to='app.Test', through='app.TestResult')),
                ('user_auth', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='testresult',
            name='user',
            field=models.ForeignKey(to='app.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(to='app.Test'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lecture',
            name='module',
            field=models.ForeignKey(to='app.Module'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='courseprogress',
            name='user',
            field=models.ForeignKey(to='app.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='app.Question'),
            preserve_default=True,
        ),
    ]
