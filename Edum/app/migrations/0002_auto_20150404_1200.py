# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='author',
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answers', to='app.Question'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='module',
            field=models.ForeignKey(related_name='lectures', to='app.Module'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='module',
            name='course',
            field=models.ForeignKey(related_name='modules', to='app.Course'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='test',
            field=models.ForeignKey(related_name='questions', to='app.Test'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='module',
            field=models.ForeignKey(related_name='tests', to='app.Module'),
            preserve_default=True,
        ),
    ]
