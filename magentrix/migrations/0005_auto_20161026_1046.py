# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 09:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magentrix', '0004_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='opportunity_ratio',
            field=models.IntegerField(null=True, verbose_name='Opportunity Ratio'),
        ),
    ]