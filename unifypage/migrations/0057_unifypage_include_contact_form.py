# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-15 10:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0056_auto_20161205_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='unifypage',
            name='include_contact_form',
            field=models.BooleanField(default=False, verbose_name='Include Contact Form'),
        ),
    ]
