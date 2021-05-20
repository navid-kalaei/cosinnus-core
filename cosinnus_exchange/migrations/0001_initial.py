# Generated by Django 2.1.15 on 2021-03-17 12:09

import cosinnus.models.mixins.indexes
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeObjectBaseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=255)),
                ('portal', models.IntegerField()),
                ('public', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('mt_location', models.CharField(max_length=255)),
                ('mt_location_lat', models.FloatField()),
                ('mt_location_lon', models.FloatField()),
                ('slug', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('contact_info', models.TextField(blank=True, null=True)),
                ('icon_image_url', models.CharField(blank=True, max_length=255, null=True)),
                ('background_image_small_url', models.CharField(blank=True, max_length=255, null=True)),
                ('background_image_large_url', models.CharField(blank=True, max_length=255, null=True)),
                ('group_slug', models.CharField(blank=True, max_length=255, null=True)),
                ('group_name', models.CharField(blank=True, max_length=255, null=True)),
                ('participant_count', models.IntegerField(default=0)),
                ('member_count', models.IntegerField(default=0)),
                ('content_count', models.IntegerField(default=0)),
                ('mt_tags', models.CharField(blank=True, max_length=255, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('mt_topics', models.CharField(blank=True, max_length=255, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('mt_visibility', models.IntegerField(default=2)),
                ('mt_public', models.BooleanField(default=True)),
            ],
            options={
                'managed': False,
            },
            bases=(cosinnus.models.mixins.indexes.IndexingUtilsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ExchangeBaseGroup',
            fields=[
                ('exchangeobjectbasemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cosinnus_exchange.ExchangeObjectBaseModel')),
            ],
            options={
                'managed': False,
            },
            bases=('cosinnus_exchange.exchangeobjectbasemodel',),
        ),
        migrations.CreateModel(
            name='ExchangeProject',
            fields=[
                ('exchangebasegroup_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cosinnus_exchange.ExchangeBaseGroup')),
            ],
            options={
                'managed': False,
            },
            bases=('cosinnus_exchange.exchangebasegroup',),
        ),
        migrations.CreateModel(
            name='ExchangeSociety',
            fields=[
                ('exchangebasegroup_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cosinnus_exchange.ExchangeBaseGroup')),
            ],
            options={
                'managed': False,
            },
            bases=('cosinnus_exchange.exchangebasegroup',),
        ),
    ]