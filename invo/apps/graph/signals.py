from channels.layers import get_channel_layer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync, sync_to_async


from waffle import get_waffle_flag_model
from waffle.models import Switch, Sample


channel_layer = get_channel_layer()


@receiver(post_save, sender=get_waffle_flag_model())
@receiver(post_delete, sender=get_waffle_flag_model())
@receiver(post_save, sender=Switch)
@receiver(post_delete, sender=Switch)
@receiver(post_save, sender=Sample)
@receiver(post_delete, sender=Sample)
def waffle_changed(sender, instance, *args, **kwargs):
    # emit that waffle models have changed
    async_to_sync(channel_layer.send)("waffle_changed", {})
