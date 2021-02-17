# Generated by Django 2.1.15 on 2020-12-16 11:45

from django.db import migrations
from cosinnus.conf import settings

def create_default_portal_conference_settings(apps, schema_editor):
    """ Creates if not exists, a CosinnusConferenceSetting object for the current portal """
    
    CosinnusPortal = apps.get_model("cosinnus", "CosinnusPortal")
    CosinnusConferenceSettings = apps.get_model("cosinnus", "CosinnusConferenceSettings")
    current_portal = CosinnusPortal.objects.get(site__id=settings.SITE_ID)
    ContentType = apps.get_model('contenttypes', 'ContentType')
    portal_content_type = ContentType.objects.get(
        app_label='cosinnus',
        model='cosinnusportal'
    )
    
    CosinnusConferenceSettings.objects.get_or_create(
        content_type=portal_content_type,
        object_id=current_portal.id,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('cosinnus', '0095_auto_20210217_1022'),
    ]

    operations = [
        migrations.RunPython(create_default_portal_conference_settings, migrations.RunPython.noop),
    ]
