# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0013_auto_20161024_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='element_type',
            field=models.IntegerField(choices=[(1, 'Box'), (2, 'Image'), (3, 'Offer'), (4, 'Counter')], verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='element',
            name='icon',
            field=models.CharField(blank=True, max_length=50, verbose_name='Icon class'),
        ),
        migrations.AlterField(
            model_name='row',
            name='row_type',
            field=models.IntegerField(choices=[(1, 'Default container'), (5, 'Parallax Counter V3'), (6, 'Parallax Counter V4'), (7, 'Gallery'), (11, 'Service Block V4'), (18, 'Team V3'), (28, 'Testimonials V6'), (29, 'Owl Carousel'), (32, 'Breadcrumb V3')], verbose_name='Type'),
        ),
    ]
