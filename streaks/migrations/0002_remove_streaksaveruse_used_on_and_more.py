# Generated by Django 4.1.3 on 2023-09-13 17:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('streaks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='streaksaveruse',
            name='used_on',
        ),
        migrations.AddField(
            model_name='streaksaveruse',
            name='crated_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userbadge',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
