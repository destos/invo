from django.contrib import admin
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
    PolymorphicParentModelAdmin,
)
from safedelete.admin import SafeDeleteAdmin, highlight_deleted

from . import models


class ItemChildAdmin(PolymorphicChildModelAdmin):
    """Base admin class for all child models"""

    base_model = models.Item
    base_readonly_fields = ("space",)
    base_fields = (
        "name",
        "data",
        "space",
    )
    base_raw_id_fields = ("sites",)


@admin.register(models.Item)
class ItemParentAdmin(SafeDeleteAdmin, PolymorphicParentModelAdmin):
    """The parent model admin"""

    base_model = models.Item
    child_models = (models.Consumable, models.TrackedConsumable, models.Tool)
    list_filter = (PolymorphicChildModelFilter,) + SafeDeleteAdmin.list_filter
    list_display = (
        highlight_deleted,
        "irn",
        "space",
    ) + SafeDeleteAdmin.list_display


@admin.register(models.Consumable)
class ConsumableAdmin(SafeDeleteAdmin, ItemChildAdmin):
    base_model = models.Consumable
    show_in_index = True
    list_display = (
        highlight_deleted,
        "count",
        "warning_count",
        "warning",
        "irn",
    ) + SafeDeleteAdmin.list_display
    raw_id_fields = ("sites",)


@admin.register(models.TrackedConsumable)
class TrackedConsumableAdmin(ConsumableAdmin):
    base_model = models.TrackedConsumable
    show_in_index = True
    raw_id_fields = ("sites",)


@admin.register(models.Tool)
class ToolAdmin(ItemChildAdmin):
    base_model = models.Tool
    show_in_index = True
    raw_id_fields = ("sites",)
