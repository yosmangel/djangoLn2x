# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0005_remove_element_background_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='element_type',
            field=models.IntegerField(choices=[(1, 'Box'), (2, 'Image'), (3, 'Offer'), (4, 'counter')], verbose_name='Type'),
        ),
    ]