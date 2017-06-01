# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-28 11:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0051_remove_row_unifypages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='row',
            name='unifypage',
        ),
        migrations.AlterField(
            model_name='rowtopage',
            name='row',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ToUnifypages', to='unifypage.Row'),
        ),
        migrations.AlterField(
            model_name='rowtopage',
            name='unifypage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ToRows', to='unifypage.UnifyPage'),
        ),
    ]
