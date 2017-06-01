# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-22 11:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0034_auto_20161122_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form',
            name='element',
        ),
        migrations.AddField(
            model_name='element',
            name='form',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='element', to='unifypage.Form'),
        ),
    ]
