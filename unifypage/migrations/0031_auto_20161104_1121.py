# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-04 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0030_auto_20161102_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='row',
            name='name',
            field=models.CharField(blank=True, help_text='A name to help differenciate the rows when setting order, must be the same as the corresponding form if the type is set to form', max_length=50, verbose_name='Name (hidden)'),
        ),
    ]