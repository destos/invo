# Generated by Django 3.1.5 on 2021-01-17 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('items', '0005_auto_20201202_2227'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consumable',
            options={},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={},
        ),
        migrations.AlterModelOptions(
            name='tool',
            options={},
        ),
        migrations.AlterModelOptions(
            name='trackedconsumable',
            options={},
        ),
        migrations.AddField(
            model_name='item',
            name='sites',
            field=models.ManyToManyField(to='sites.Site'),
        ),
    ]