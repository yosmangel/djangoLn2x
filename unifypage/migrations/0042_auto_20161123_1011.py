# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-23 10:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0041_auto_20161122_1725'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='input',
            options={'ordering': ('_order',), 'verbose_name': 'Input', 'verbose_name_plural': 'Inputs'},
        ),
        migrations.AddField(
            model_name='input',
            name='rows',
            field=models.IntegerField(blank=True, null=True, verbose_name='Number of rows'),
        ),
    ]
