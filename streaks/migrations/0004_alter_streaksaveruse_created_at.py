# Generated by Django 4.1.3 on 2023-09-19 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaks', '0003_rename_crated_at_streaksaveruse_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streaksaveruse',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
