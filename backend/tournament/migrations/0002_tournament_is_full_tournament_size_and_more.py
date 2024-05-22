# Generated by Django 4.2.7 on 2024-04-25 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='is_full',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tournament',
            name='size',
            field=models.CharField(choices=[('four', 'Four'), ('height', 'Height')], default='four', max_length=10),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='status',
            field=models.CharField(choices=[('looking_for_players', 'Looking for players'), ('in_progress', 'In progress'), ('over', 'Over'), ('cancelled', 'Cancelled')], default='looking_for_players', max_length=20),
        ),
    ]
