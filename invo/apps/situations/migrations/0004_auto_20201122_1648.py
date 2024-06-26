# Generated by Django 3.1.3 on 2020-11-22 22:48

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_auto_20201023_0254'),
        ('spaces', '0006_auto_20201122_1237'),
        ('situations', '0003_auto_20201122_1237'),
    ]

    operations = [
        migrations.CreateModel(
            name='SelectedSpace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('situation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='situations.situation')),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaces.spacenode')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SelectedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.item')),
                ('situation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='situations.situation')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='situation',
            name='items',
            field=models.ManyToManyField(related_name='situations', through='situations.SelectedItem', to='items.Item'),
        ),
        migrations.AddField(
            model_name='situation',
            name='spaces',
            field=models.ManyToManyField(related_name='situations', through='situations.SelectedSpace', to='spaces.SpaceNode'),
        ),
    ]
