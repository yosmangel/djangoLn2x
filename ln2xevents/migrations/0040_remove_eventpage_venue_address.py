# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-15 14:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ln2xevents', '0039_eventpage_venue_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventpage',
            name='venue_address',
        ),
    ]
