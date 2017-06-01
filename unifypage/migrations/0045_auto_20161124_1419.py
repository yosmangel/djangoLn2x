# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-24 14:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0044_input_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='input',
            name='name',
            field=models.CharField(blank=True, max_length=200, verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='input',
            name='value_en',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Default Value'),
        ),
        migrations.AddField(
            model_name='input',
            name='value_es',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Default Value'),
        ),
        migrations.AddField(
            model_name='input',
            name='value_fr',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Default Value'),
        ),
    ]
