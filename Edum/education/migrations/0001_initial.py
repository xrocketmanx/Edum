# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('answer', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('overview', models.TextField()),
                ('duration', models.TimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseProgress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('progress', models.IntegerField()),
                ('course', models.ForeignKey(to='app.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('test_count', models.IntegerField()),
                ('lecture_count', models.IntegerField()),
                ('name', models.TextField()),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('question', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('question_count', models.IntegerField()),
                ('module', models.ForeignKey(to='app.Module')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('passed', models.BooleanField()),
                ('test', models.ForeignKey(to='app.Test')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('first_name', models.CharField(max_length=40)),
                ('second_name', models.CharField(max_length=40)),
                ('login', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=16)),
                ('courses_results', models.ManyToManyField(through='app.CourseProgress', to='app.Course')),
                ('signed_courses', models.ManyToManyField(related_name='signed_courses', to='app.Course')),
                ('tests_results', models.ManyToManyField(through='app.TestResult', to='app.Test')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='testresult',
            name='user',
            field=models.ForeignKey(to='app.User'),
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
            field=models.ForeignKey(to='app.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.OneToOneField(to='app.Question'),
            preserve_default=True,
        ),
    ]
