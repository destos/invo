# Generated by Django 3.1.3 on 2020-11-29 17:31

from django.db import migrations, models
import spaces.models


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0006_auto_20201122_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spacenode',
            name='data',
            field=models.JSONField(blank=True, default=spaces.models.default_data),
        ),
    ]
