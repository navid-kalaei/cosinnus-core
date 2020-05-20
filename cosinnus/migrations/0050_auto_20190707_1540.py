# Generated by Django 2.1.5 on 2019-07-07 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosinnus', '0049_auto_20190529_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='cosinnusportal',
            name='welcome_email_active',
            field=models.BooleanField(default=False, verbose_name='Welcome-Email sending enabled'),
        ),
        migrations.AlterField(
            model_name='cosinnusportal',
            name='welcome_email_text',
            field=models.TextField(blank=True, help_text='If set and enabled, this text will be sent to all new users after their registration is complete.', null=True, verbose_name='Welcome-Email Text'),
        ),
    ]