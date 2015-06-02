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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('duration', models.FloatField(default=0)),
                ('overview', models.TextField()),
                ('rating', models.IntegerField(default=0)),
                ('author', models.ForeignKey(default=0, to=settings.AUTH_USER_MODEL, related_name='courses')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('progress', models.IntegerField(default=0)),
                ('course', models.ForeignKey(to='app.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CoursesLikes',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('course', models.ForeignKey(to='app.Course')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('overview', models.TextField()),
                ('course', models.ForeignKey(to='app.Course', related_name='modules')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('question_count', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=250)),
                ('duration', models.IntegerField()),
                ('module', models.ForeignKey(to='app.Module', related_name='tests')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('courses_results', models.ManyToManyField(to='app.Course', through='app.CourseProgress')),
                ('signed_courses', models.ManyToManyField(to='app.Course', related_name='signed_courses')),
                ('tests_results', models.ManyToManyField(to='app.Test', through='app.TestResult')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='user_profile')),
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
            field=models.ForeignKey(to='app.Test', related_name='questions'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lecture',
            name='module',
            field=models.ForeignKey(to='app.Module', related_name='lectures'),
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
            field=models.ForeignKey(to='app.Question', related_name='answers'),
            preserve_default=True,
        ),
    ]
