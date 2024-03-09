from decimal import Decimal as D

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from polymorphic.models import PolymorphicModel
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

from invo.utils.pghistory import enable_history

from ..managers import CurrentSiteItemManager, ItemManager
from owners.models import SharedSite
from protocol.models import Protocol


@enable_history(related_name="item_history")
class Item(SharedSite, Protocol, TimeStampedModel, PolymorphicModel, SafeDeleteModel):
    """Base item that can be stored in different spaces"""

    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(_("Name"), max_length=50)
    data = models.JSONField(null=True, blank=True)

    # Many to many? can an item be inside multiple spaces? currently spaces are nested
    # so that could result in issues
    space = models.ForeignKey(
        "spaces.SpaceNode",
        blank=True,
        null=True,
        related_name="items",
        on_delete=models.DO_NOTHING,
    )

    declaration = models.ForeignKey(
        "items.Declaration",
        blank=True,
        null=True,
        related_name="items",
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return self.name

    @property
    def description(self):
        return ""

    objects = ItemManager()
    current_site_objects = CurrentSiteItemManager()


@enable_history(related_name="consumable_history")
class Consumable(Item):
    """Tracks the amount of a particular item, usually placed all together."""

    # What about Units? What about non-integer amounts?
    count = models.DecimalField(default=D("0"), max_digits=13, decimal_places=4)
    warning_enabled = models.BooleanField(default=False)
    warning_count = models.DecimalField(default=D("1"), max_digits=13, decimal_places=4)

    def consume(self, amount=1, save=True):
        self.count -= amount
        if save:
            self.save(
                update_fields=(
                    "count",
                    "modified",
                )
            )

    def addition(self, amount=1, save=True):
        self.count += amount
        if save:
            self.save(
                update_fields=(
                    "count",
                    "modified",
                )
            )

    @property
    def warning(self):
        return self.warning_enabled and self.count <= self.warning_count


@enable_history(related_name="tracked_consumable_history")
class TrackedConsumable(Consumable):
    """Serialized consumable consumption for tracking"""

    # Notes:
    # Tracked items and consumables maybe need to exist in multiple spaces?
    # that is outside the nesting scheme, how to handle that?
    # Do tracked consumables have a single instance per item?
    # Count may be able to tracked via relation to equipment in the future?
    # or synced from it, becomes normalized field

    def consume(self, *equipment, **kwargs):
        return super().consume(amount=len(equipment), **kwargs)

    def addition(self, *equipment, **kwargs):
        return super().consume(amount=len(equipment), **kwargs)


@enable_history(related_name="tool_history")
class Tool(Item):
    """Tools allow you to store """

    # TODO: toolhub tool taxonomy system, mqtt yo! make it better this time.
    pass


__all__ = ["Item", "Consumable", "TrackedConsumable", "Tool"]
