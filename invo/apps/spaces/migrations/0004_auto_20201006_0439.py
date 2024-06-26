# Generated by Django 3.1.2 on 2020-10-06 04:39

from django.db import migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0003_auto_20201006_0325'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gridspacenode',
            options={'get_latest_by': 'modified'},
        ),
        migrations.AddField(
            model_name='spacenode',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spacenode',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
    ]
