# Generated by Django 4.2.7 on 2024-03-14 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_account_nb_try_2fa_account_qrcode_2fa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='secret_2FA',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True),
        ),
    ]
