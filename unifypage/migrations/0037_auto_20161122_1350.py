# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-22 13:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0036_auto_20161122_1155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form',
            name='element',
        ),
        migrations.AddField(
            model_name='element',
            name='form',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='unifypage.Form'),
        ),
    ]
