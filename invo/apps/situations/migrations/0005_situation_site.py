# Generated by Django 3.1.5 on 2021-01-24 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('situations', '0004_auto_20201122_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='situation',
            name='site',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sites.site'),
            preserve_default=False,
        ),
    ]
