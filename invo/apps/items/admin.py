from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from .models import Item, Consumable, Tool, TrackedConsumable
from safedelete.admin import SafeDeleteAdmin, highlight_deleted


class ItemChildAdmin(PolymorphicChildModelAdmin):
    """Base admin class for all child models"""
    base_model = Item  # Optional, explicitly set here.

    # By using these `base_...` attributes instead of the regular Itemdmin `form` and `fieldsets`,
    # the additional fields of the child models are automatically added to the admin form.
    # base_form = ...
    base_fields = (
        "name", "data", "space"
    )


@admin.register(Item)
class ItemParentAdmin(SafeDeleteAdmin, PolymorphicParentModelAdmin):
    """The parent model admin"""
    base_model = Item 
    child_models = (Consumable, TrackedConsumable, Tool)
    list_filter = (PolymorphicChildModelFilter,) + SafeDeleteAdmin.list_filter 
    list_display = (highlight_deleted,) + SafeDeleteAdmin.list_display


@admin.register(Consumable)
class ConsumableAdmin(SafeDeleteAdmin, ItemChildAdmin):
    base_model = Consumable
    show_in_index = True
    list_display = (highlight_deleted, "count", "warning_count", "warning") + SafeDeleteAdmin.list_display
    

@admin.register(TrackedConsumable)
class TrackedConsumableAdmin(ConsumableAdmin):
    base_model = TrackedConsumable
    show_in_index = True


@admin.register(Tool)
class ToolAdmin(ItemChildAdmin):
    base_model = Tool
    show_in_index = True
