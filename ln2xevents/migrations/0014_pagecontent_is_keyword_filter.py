# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-12 10:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ln2xevents', '0013_auto_20170111_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagecontent',
            name='is_keyword_filter',
            field=models.BooleanField(default=False),
        ),
    ]
