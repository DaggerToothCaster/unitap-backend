# Generated by Django 4.0.4 on 2023-05-08 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_userprofile_username_alter_wallet_wallet_type'),
        ('tokenTap', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tokendistribution',
            name='discord_url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tokendistribution',
            name='distributer',
            field=models.CharField(default='0', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tokendistribution',
            name='distributer_url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tokendistribution',
            name='image_url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tokendistribution',
            name='twitter_url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='TokenDistributionClaim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('typed_signed_data', models.TextField()),
                ('token_distribution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claims', to='tokenTap.tokendistribution')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tokentap_claims', to='authentication.userprofile')),
            ],
        ),
    ]
