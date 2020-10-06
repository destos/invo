# Generated by Django 3.1.2 on 2020-10-05 02:53

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0002_gridspacenode_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gridspacenode',
            name='grid_size',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(), null=True, size=2),
        ),
    ]
