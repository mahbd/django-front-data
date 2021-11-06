# Generated by Django 3.2.9 on 2021-11-06 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('description', models.TextField(blank=True, null=True)),
                ('key', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('key',),
            },
        ),
    ]
