# Generated by Django 2.1.15 on 2021-02-17 09:22

import cosinnus.models.mixins.indexes
import cosinnus.utils.bigbluebutton
from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('cosinnus', '0094_auto_20210215_1135'),
    ]

    operations = [
        migrations.CreateModel(
            name='CosinnusConferenceSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('bbb_server_choice', models.PositiveSmallIntegerField(choices=[(0, '(None)')], default=0, help_text='The chosen BBB-Server/Cluster setting for the generic object. WARNING: changing this will cause new meeting connections to use the new server, even for ongoing meetings on the old server, essentially splitting a running meeting in two!', verbose_name='BBB Server')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Cosinnus Conference Setting',
                'verbose_name_plural': 'Cosinnus Conference Settings',
            },
        ),
        migrations.RemoveField(
            model_name='cosinnusportal',
            name='bbb_server',
        ),
        migrations.AlterUniqueTogether(
            name='cosinnusconferencesettings',
            unique_together={('content_type', 'object_id')},
        ),
    ]
