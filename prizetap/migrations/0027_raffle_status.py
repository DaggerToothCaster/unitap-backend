# Generated by Django 4.0.4 on 2023-09-18 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prizetap', '0026_alter_raffle_nft_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='raffle',
            name='status',
            field=models.CharField(choices=[('OPEN', 'Open'), ('REJECTED', 'Rejected'), ('HELD', 'Held'), ('WS', 'Winner is set')], default='OPEN', max_length=10),
        ),
    ]