# Generated by Django 2.1.15 on 2021-03-17 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cosinnus_exchange', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeEvent',
            fields=[
                ('exchangeobjectbasemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cosinnus_exchange.ExchangeObjectBaseModel')),
            ],
            options={
                'managed': False,
            },
            bases=('cosinnus_exchange.exchangeobjectbasemodel',),
        ),
        migrations.CreateModel(
            name='ExchangeOrganization',
            fields=[
                ('exchangeobjectbasemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cosinnus_exchange.ExchangeObjectBaseModel')),
            ],
            options={
                'managed': False,
            },
            bases=('cosinnus_exchange.exchangeobjectbasemodel',),
        ),
    ]