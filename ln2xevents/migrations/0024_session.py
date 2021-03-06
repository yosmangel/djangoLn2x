# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-26 11:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ln2xevents', '0023_auto_20170125_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salesforce_id', models.CharField(max_length=18, null=True, unique=True)),
                ('last_sync', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Last Sync')),
                ('name', models.CharField(blank=True, max_length=80, null=True, verbose_name='Session Number')),
                ('content_reference', models.URLField(blank=True, null=True, verbose_name='Content Reference')),
                ('published', models.BooleanField(default=False)),
                ('session_abstract', models.TextField(blank=True, null=True, verbose_name='Session Abstract')),
                ('session_code', models.CharField(blank=True, max_length=30, null=True, verbose_name='Session Code')),
                ('session_end_time', models.DateTimeField(blank=True, null=True, verbose_name='Session End Time')),
                ('session_format', models.CharField(blank=True, choices=[('Case study with customer(s)', 'Case study with customer(s)'), ('Hands-on training', 'Hands-on training'), ('Panel with customers', 'Panel with customers'), ('Demo with customer(s)', 'Demo with customer(s)'), ('Presentation without customer(s)', 'Presentation without customer(s)'), ('BREAK', 'BREAK')], max_length=255, null=True, verbose_name='Session Format')),
                ('session_slot_number', models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')], max_length=255, null=True, verbose_name='Session Slot Number')),
                ('session_start_time', models.DateTimeField(blank=True, null=True, verbose_name='Session Start Time')),
                ('session_take', models.TextField(blank=True, null=True, verbose_name='Session Takeaways')),
                ('session_theme', models.CharField(blank=True, choices=[('Product Roadmap', 'Product Roadmap'), ('Mobile', 'Mobile'), ('AppExchange', 'AppExchange'), ('Apex', 'Apex'), ('SSS', 'SSS'), ('PRM', 'PRM'), ('UE', 'UE'), ('Marketing', 'Marketing'), ('Core Needs', 'Core Needs'), ('Vertical', 'Vertical'), ('New Release', 'New Release')], max_length=255, null=True, verbose_name='Session Theme')),
                ('sponsored', models.BooleanField(default=False)),
                ('session_public_name', models.TextField(blank=True, null=True, verbose_name='Session Public Name')),
                ('session_image', models.URLField(blank=True, null=True, verbose_name='SessionImage')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ln2xevents.CoursePage')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ln2xevents.EventPage')),
            ],
            options={
                'verbose_name': 'Session',
                'verbose_name_plural': 'Sessions',
            },
        ),
    ]
