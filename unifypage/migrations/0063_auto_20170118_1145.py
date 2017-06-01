# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-18 11:45
from __future__ import unicode_literals

from django.db import migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0062_auto_20170118_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='unifypage',
            name='intro_en',
            field=mezzanine.core.fields.RichTextField(blank=True, null=True, verbose_name='Introduction text'),
        ),
        migrations.AddField(
            model_name='unifypage',
            name='intro_es',
            field=mezzanine.core.fields.RichTextField(blank=True, null=True, verbose_name='Introduction text'),
        ),
        migrations.AddField(
            model_name='unifypage',
            name='intro_fr',
            field=mezzanine.core.fields.RichTextField(blank=True, null=True, verbose_name='Introduction text'),
        ),
    ]