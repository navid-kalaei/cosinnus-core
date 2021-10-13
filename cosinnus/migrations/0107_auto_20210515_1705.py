# Generated by Django 2.1.15 on 2021-05-15 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cosinnus', '0106_mark_inactive_users_for_deletion'),
    ]

    operations = [
        migrations.CreateModel(
            name='CosinnusConferencePremiumBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateTimeField(blank=True, default=None, help_text='During this time, the conference will be using the premium BBB server.', null=True, verbose_name='Start Datetime')),
                ('to_date', models.DateTimeField(blank=True, default=None, help_text='During this time, the conference will be using the premium BBB server.', null=True, verbose_name='End Datetime')),
                ('participants', models.PositiveIntegerField(default=0, help_text='The number of BBB participants that have been declared will take part in the conference during this time. This is only a guideline for portal admins.', verbose_name='Conference participants')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last modified')),
            ],
            options={
                'verbose_name': 'Cosinnus Conference Premium Block',
                'verbose_name_plural': 'Cosinnus Conference Premium Blocks',
                'ordering': ('from_date',),
            },
        ),
        migrations.CreateModel(
            name='CosinnusConferencePremiumCapacityInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateTimeField(blank=True, default=None, help_text='The time frame while the selected capacity is available.', null=True, verbose_name='Start Datetime')),
                ('to_date', models.DateTimeField(blank=True, default=None, help_text='The time frame while the selected capacity is available.', null=True, verbose_name='End Datetime')),
                ('max_participants', models.PositiveIntegerField(default=0, help_text='The maximum number of BBB participants that should be allowed for all premium conferences. This is only a guideline for portal admins.', verbose_name='Maximum BBB participants')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last modified')),
            ],
            options={
                'verbose_name': 'Cosinnus Conference Premium Capacity Info',
                'verbose_name_plural': 'Cosinnus Conference Premium Capacity Infos',
                'ordering': ('from_date',),
            },
        ),
        migrations.AddField(
            model_name='cosinnusconferencepremiumcapacityinfo',
            name='portal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portal_premium_capacity_blocks', to='cosinnus.CosinnusPortal', verbose_name='Portal'),
        ),
        migrations.AddField(
            model_name='cosinnusconferencepremiumblock',
            name='conference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conference_premium_blocks', to=settings.COSINNUS_GROUP_OBJECT_MODEL, verbose_name='Conference'),
        ),
    ]
