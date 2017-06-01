# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-17 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0060_auto_20170116_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='unifypage',
            name='miniature_url',
            field=models.CharField(blank=True, max_length=200, verbose_name='Miniature URL'),
        ),
        migrations.AlterField(
            model_name='element',
            name='element_type',
            field=models.IntegerField(choices=[(5, 'Row Dependant'), (2, 'Image'), (4, 'Counter'), (6, 'Vertical Progress Bar'), (7, 'Testimonial'), (1, 'Box'), (8, 'Course Block'), (9, 'Form'), (10, 'Image zoom')], verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='row',
            name='background',
            field=models.CharField(blank=True, help_text='CSS background property<br/>Can take: url(your_image_url), <br/>A color name (exemple grey), <br/>rgba(red, green, blue, opacity) with red, green and blue between 0 and 255 and opacity between 0 and 1,<br/>#hexvalue...', max_length=500, verbose_name='Background'),
        ),
    ]
