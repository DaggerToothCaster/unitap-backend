# Generated by Django 4.0.4 on 2023-10-10 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0019_rename_is_temporary_userprofile_is_new_by_wallet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_new_by_wallet',
        ),
    ]
