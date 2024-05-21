# Generated by Django 4.2.7 on 2024-05-19 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_remove_roommessages_message_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='roommessages',
            name='message_type',
            field=models.CharField(choices=[('text', 'text'), ('invitation', 'invitation'), ('tournament', 'tournament')], default='text', max_length=10),
        ),
        migrations.AddField(
            model_name='roommessages',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'pending'), ('accepted', 'accepted'), ('rejected', 'rejected'), ('expired', 'expired')], max_length=10, null=True),
        ),
    ]