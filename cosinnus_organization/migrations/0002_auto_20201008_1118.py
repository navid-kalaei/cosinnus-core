# Generated by Django 2.1.15 on 2020-10-08 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.COSINNUS_GROUP_OBJECT_MODEL),
        ('cosinnus_organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CosinnusOrganizationGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'pending'), (1, 'member'), (2, 'admin'), (3, 'pending-invited')], db_index=True, default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizations', to=settings.COSINNUS_GROUP_OBJECT_MODEL)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='cosinnus_organization.CosinnusOrganization')),
            ],
            options={
                'verbose_name': 'Organization membership',
                'verbose_name_plural': 'Organization memberships',
            },
        ),
        migrations.AlterUniqueTogether(
            name='cosinnusorganizationgroup',
            unique_together={('organization', 'group')},
        ),
    ]