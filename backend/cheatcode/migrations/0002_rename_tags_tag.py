# Generated by Django 4.0.5 on 2022-06-27 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheatcode', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tags',
            new_name='Tag',
        ),
    ]