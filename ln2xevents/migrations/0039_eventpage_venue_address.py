# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-12 10:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ln2xevents', '0038_auto_20170215_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='venue_address',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='Address'),
        ),
    ]
