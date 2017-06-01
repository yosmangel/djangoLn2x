# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-22 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0037_auto_20161122_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Name (hidden)'),
        ),
        migrations.AlterField(
            model_name='element',
            name='is_formula',
            field=models.BooleanField(default=False, help_text='Contains a formula', verbose_name='Formula'),
        ),
    ]
