# Generated by Django 3.1.7 on 2021-03-27 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0008_consumableevent_itemevent_toolevent_trackedconsumableevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumableevent',
            name='pgh_obj',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='consumable_history', to='items.consumable'),
        ),
        migrations.AlterField(
            model_name='itemevent',
            name='pgh_obj',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='item_history', to='items.item'),
        ),
        migrations.AlterField(
            model_name='toolevent',
            name='pgh_obj',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='tool_history', to='items.tool'),
        ),
        migrations.AlterField(
            model_name='trackedconsumableevent',
            name='pgh_obj',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='tracked_consumable_history', to='items.trackedconsumable'),
        ),
    ]
