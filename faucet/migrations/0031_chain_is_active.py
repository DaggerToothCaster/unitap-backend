# Generated by Django 4.0.4 on 2022-12-17 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faucet', '0030_chain_gas_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='chain',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]