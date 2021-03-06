# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-22 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0040_auto_20161122_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='element',
            name='is_form',
        ),
        migrations.AlterField(
            model_name='element',
            name='element_type',
            field=models.IntegerField(choices=[(5, 'Row Dependant'), (2, 'Image'), (4, 'Counter'), (6, 'Vertical Progress Bar'), (7, 'Testimonial'), (1, 'Box'), (8, 'Course Block'), (9, 'Form')], verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='input',
            name='input_type',
            field=models.IntegerField(choices=[(1, 'Text Input'), (2, 'Text Area'), (3, 'Email'), (4, 'Checkbox')], verbose_name='Type'),
        ),
    ]
