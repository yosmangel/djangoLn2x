# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-25 15:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

def make_many_rows(apps, schema_editor):
    """
    Adds the Unifypage object in Row.unifypage to the
    many-to-many relationship in Row.unifypages
    """
    Row = apps.get_model('unifypage', 'Row')

    for row in Row.objects.all():
        row.unifypages.add(row.unifypage)

class Migration(migrations.Migration):

    dependencies = [
        ('unifypage', '0045_auto_20161124_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='row',
            name='unifypages',
            field=models.ManyToManyField(related_name='rows', to='unifypage.UnifyPage'),
        ),
        migrations.AlterField(
            model_name='row',
            name='row_type',
            field=models.IntegerField(choices=[(1, 'Default container'), (34, 'Block grid V2'), (5, 'Parallax Counter V3'), (6, 'Parallax Counter V4'), (7, 'Gallery'), (11, 'Service Block V4'), (18, 'Team V3'), (28, 'Testimonials V6'), (29, 'Owl Carousel'), (32, 'Breadcrumb V3'), (36, 'Basic Map')], verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='row',
            name='unifypage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='row', to='unifypage.UnifyPage'),
        ),
        migrations.RunPython(make_many_rows),
    ]
