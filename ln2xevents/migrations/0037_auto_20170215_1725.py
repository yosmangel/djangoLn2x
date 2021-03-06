# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 17:25
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ln2xevents', '0036_auto_20170214_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursepage',
            name='agenda',
            field=mezzanine.core.fields.RichTextField(blank=True, null=True, verbose_name='Agenda'),
        ),
        migrations.AddField(
            model_name='coursepage',
            name='course_level',
            field=models.CharField(blank=True, choices=[('Advanced', 'Advanced'), ('Foundation', 'Foundation'), ('Professional', 'Professional')], max_length=50, null=True, verbose_name='Course Level'),
        ),
        migrations.AddField(
            model_name='coursepage',
            name='duration',
            field=models.IntegerField(default=0, verbose_name='Duration(min)'),
        ),
        migrations.AddField(
            model_name='coursepage',
            name='languages_availables',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Languages Availables'),
        ),
        migrations.AddField(
            model_name='coursepage',
            name='objectives',
            field=mezzanine.core.fields.RichTextField(blank=True, null=True, verbose_name='Objectives'),
        ),
        migrations.AddField(
            model_name='coursepage',
            name='pre_requisites',
            field=mezzanine.core.fields.RichTextField(blank=True, null=True, verbose_name='Pre-requisites'),
        ),
        migrations.AddField(
            model_name='coursepage',
            name='ref_source',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ref/Source'),
        ),
        migrations.AddField(
            model_name='coursepage',
            name='subject_category',
            field=models.CharField(blank=True, choices=[('Payment System Security, Risk & Compliance', 'Payment System Security, Risk & Compliance'), ('Payment System Management', 'Payment System Management'), ('Information Security and Privacy', 'Information Security and Privacy'), ('Secure Coding & Testing', 'Secure Coding & Testing')], max_length=255, null=True, verbose_name='Subject Category'),
        ),
        migrations.AddField(
            model_name='coursepage',
            name='who_attends',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Who Attends'),
        ),
    ]
