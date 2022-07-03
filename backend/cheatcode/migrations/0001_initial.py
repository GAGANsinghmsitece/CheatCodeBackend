# Generated by Django 4.0.5 on 2022-06-27 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('difficulty', models.CharField(choices=[('1', 'Easy'), ('2', 'Medium'), ('3', 'Hard')], max_length=1)),
                ('like', models.IntegerField()),
                ('unlike', models.IntegerField()),
                ('tags', models.ManyToManyField(to='cheatcode.tags')),
            ],
        ),
    ]
