# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-03 12:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0066_remove_multilangkeyword_blog_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='multilangkeyword',
            name='icon_url',
            field=models.CharField(blank=True, max_length=200, verbose_name='Icon URL'),
        ),
    ]