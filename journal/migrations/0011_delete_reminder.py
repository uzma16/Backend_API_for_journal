# Generated by Django 4.1.3 on 2023-09-13 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0010_remove_journal_entry_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Reminder',
        ),
    ]
