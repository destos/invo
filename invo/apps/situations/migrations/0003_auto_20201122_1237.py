# Generated by Django 3.1.3 on 2020-11-22 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('situations', '0002_auto_20201028_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='situation',
            name='items',
        ),
        migrations.RemoveField(
            model_name='situation',
            name='spaces',
        ),
    ]
