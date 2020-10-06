
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from polymorphic.models import PolymorphicModel
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE


class Item(TimeStampedModel, PolymorphicModel, SafeDeleteModel):
    """Base item that can be stored in different spaces"""
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(_("Name"), max_length=50)
    data = models.JSONField(null=True, blank=True)

    space = models.ForeignKey(
        "spaces.SpaceNode", blank=True, null=True, related_name="items", on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class Consumable(Item):
    """Stores extra data related to if an item"""
    count = models.PositiveIntegerField(default=0)
    warning_enabled = models.BooleanField(default=False)
    warning_count = models.PositiveIntegerField(default=10)

    def consume(self, amount=1, save=True):
        self.count -= amount
        if save:
            self.save(update_fields=("count", "modified",))


    def addition(self, amount=1, save=True):
        self.count += amount
        if save:
            self.save(update_fields=("count", "modified",))
    
    @property
    def warning(self):
        return self.warning_enabled and self.warning_count >= self.count


class TrackedConsumable(Consumable):
    """Serialized consumable consumption for tracking"""
    # Count may be able to tracked via relation to equipment in the future?

    def consume(self, *equipment, **kwargs):
        return super().consume(amount=len(equipment), **kwargs)

    def addition(self, *equipment, **kwargs):
        return super().consume(amount=len(equipment), **kwargs)


class Tool(Item):
    """Tools yo"""
    # TODO: tools taxonomy system
    pass