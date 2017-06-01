# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-19 14:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ln2xevents', '0005_lnximage_mark_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseImageBreaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField(blank=True, max_length=500, verbose_name='Image URL')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='ln2xevents.CoursePage')),
            ],
        ),
    ]
