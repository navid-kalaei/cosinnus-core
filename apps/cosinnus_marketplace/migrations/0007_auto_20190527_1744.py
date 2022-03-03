# Generated by Django 2.1.5 on 2019-05-27 15:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cosinnus_marketplace', '0006_offer_last_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='last_action',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='A datetime for when a significant action last happened for this object, which users might be interested in. I.e. new comments, special edits, etc.', verbose_name='Last action happened'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offer',
            name='last_action_user',
            field=models.ForeignKey(help_text='The user which caused the last significant action to update the `last_action` datetime.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Last action user'),
        ),
    ]
