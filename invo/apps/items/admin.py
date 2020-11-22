from django.contrib import admin
from polymorphic.admin import (
    PolymorphicParentModelAdmin,
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
)
from . import models
from safedelete.admin import SafeDeleteAdmin, highlight_deleted


class ItemChildAdmin(PolymorphicChildModelAdmin):
    """Base admin class for all child models"""

    base_model = models.Item
    base_readonly_fields = ("space",)
    base_fields = (
        "name",
        "data",
        "space",
    )


@admin.register(models.Item)
class ItemParentAdmin(SafeDeleteAdmin, PolymorphicParentModelAdmin):
    """The parent model admin"""

    base_model = models.Item
    child_models = (models.Consumable, models.TrackedConsumable, models.Tool)
    list_filter = (PolymorphicChildModelFilter,) + SafeDeleteAdmin.list_filter
    list_display = (
        highlight_deleted,
        "urn",
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
        "urn",
    ) + SafeDeleteAdmin.list_display


@admin.register(models.TrackedConsumable)
class TrackedConsumableAdmin(ConsumableAdmin):
    base_model = models.TrackedConsumable
    show_in_index = True


@admin.register(models.Tool)
class ToolAdmin(ItemChildAdmin):
    base_model = models.Tool
    show_in_index = True
