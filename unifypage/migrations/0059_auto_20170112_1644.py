# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-12 16:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0058_auto_20170112_1550'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='multilangkeyword',
            options={'ordering': ('word',), 'verbose_name': 'Multilang Keyword', 'verbose_name_plural': 'Multilang Keywords'},
        ),
    ]
