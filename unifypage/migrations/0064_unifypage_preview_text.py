# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-20 15:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0063_auto_20170118_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='unifypage',
            name='preview_text',
            field=models.CharField(blank=True, max_length=50, verbose_name='Preview Text'),
        ),
    ]
