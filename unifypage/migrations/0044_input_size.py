# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-23 11:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0043_element_button_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='input',
            name='size',
            field=models.IntegerField(default=12, verbose_name='Size(1-12)'),
        ),
    ]
