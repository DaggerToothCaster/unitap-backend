# Generated by Django 4.0.4 on 2023-05-11 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faucet', '0045_chain_tokentap_contract_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalsettings',
            name='tokentap_weekly_claim_limit',
            field=models.IntegerField(default=2),
        ),
    ]