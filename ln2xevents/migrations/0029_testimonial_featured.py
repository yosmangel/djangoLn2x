# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-02 10:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ln2xevents', '0028_eventpage_multilang_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonial',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='Featured'),
        ),
    ]
