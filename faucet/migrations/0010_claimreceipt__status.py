# Generated by Django 4.0.4 on 2022-04-17 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faucet', '0009_chain_wallet_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='claimreceipt',
            name='_status',
            field=models.CharField(choices=[('0', 'Pending'), ('1', 'Verified'), ('2', 'Rejected')], default='0', max_length=1),
        ),
    ]