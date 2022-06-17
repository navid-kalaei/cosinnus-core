# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-05 12:10
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('cosinnus_stream', '0006_auto_20180926_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='portals',
            field=models.CharField(blank=True, default='', max_length=255, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Portal IDs'),
        ),
        migrations.AlterField(
            model_name='stream',
            name='special_groups',
            field=models.CharField(blank=True, default='', max_length=255, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Special Group IDs'),
        ),
    ]