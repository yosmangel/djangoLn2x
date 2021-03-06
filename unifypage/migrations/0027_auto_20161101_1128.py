# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-01 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0026_auto_20161101_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='icon_url',
            field=models.CharField(blank=True, max_length=200, verbose_name='Icon URL'),
        ),
        migrations.AlterField(
            model_name='element',
            name='more_url',
            field=models.CharField(blank=True, max_length=200, verbose_name='Link to more'),
        ),
        migrations.AlterField(
            model_name='element',
            name='more_url_en',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Link to more'),
        ),
        migrations.AlterField(
            model_name='element',
            name='more_url_es',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Link to more'),
        ),
        migrations.AlterField(
            model_name='element',
            name='more_url_fr',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Link to more'),
        ),
        migrations.AlterField(
            model_name='row',
            name='more_url',
            field=models.CharField(blank=True, max_length=200, verbose_name='Link to more'),
        ),
        migrations.AlterField(
            model_name='row',
            name='more_url_en',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Link to more'),
        ),
        migrations.AlterField(
            model_name='row',
            name='more_url_es',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Link to more'),
        ),
        migrations.AlterField(
            model_name='row',
            name='more_url_fr',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Link to more'),
        ),
    ]
