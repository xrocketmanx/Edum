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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('overview', models.TextField()),
                ('duration', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseProgress',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('test_count', models.IntegerField(default=0)),
                ('lecture_count', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=250)),
                ('overview', models.TextField()),
                ('course', models.ForeignKey(related_name='modules', to='app.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('question_count', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=250)),
                ('duration', models.IntegerField()),
                ('module', models.ForeignKey(related_name='tests', to='app.Module')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
            field=models.ForeignKey(related_name='questions', to='app.Test'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lecture',
            name='module',
            field=models.ForeignKey(related_name='lectures', to='app.Module'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='courseprogress',
            name='user',
            field=models.ForeignKey(to='app.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='author',
            field=models.ForeignKey(related_name='courses', to='app.UserProfile', default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answers', to='app.Question'),
            preserve_default=True,
        ),
    ]
