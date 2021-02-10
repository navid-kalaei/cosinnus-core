# Generated by Django 2.1.15 on 2021-02-09 09:37

import cosinnus.models.mixins.indexes
import cosinnus.utils.bigbluebutton
import cosinnus.utils.files
from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        ('cosinnus', '0090_auto_20210204_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='participationmanagement',
            name='application_conditions_upload',
            field=models.FileField(blank=True, help_text='Shown as a download link near the checkbox to accept the conditions.', max_length=250, null=True, upload_to=cosinnus.utils.files.get_conference_conditions_filename, verbose_name='Conditiions for participation'),
        )
    ]
