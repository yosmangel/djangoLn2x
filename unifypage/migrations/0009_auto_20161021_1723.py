# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 16:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0008_auto_20161021_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='row',
            name='row_type',
            field=models.IntegerField(choices=[(1, 'Default container'), (2, 'Parallax Counter'), (3, 'Parallax Counter V1'), (4, 'Parallax Counter V2'), (5, 'Parallax Counter V3'), (6, 'Parallax Counter V4'), (7, 'Gallery')], verbose_name='Type'),
        ),
    ]
