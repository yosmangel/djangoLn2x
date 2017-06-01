# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-26 11:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ln2xevents', '0024_session'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='session_abstract',
            new_name='abstract',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='session_code',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='session_end_time',
            new_name='end_time',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='session_image',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='session_public_name',
            new_name='public_name',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='session_slot_number',
            new_name='slot_number',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='session_start_time',
            new_name='start_time',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='session_take',
            new_name='take',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='session_theme',
            new_name='theme',
        ),
    ]
