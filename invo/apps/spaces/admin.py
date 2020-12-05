from django.contrib import admin

from django.utils.translation import ugettext_lazy as _
from polymorphic_tree.admin import (
    PolymorphicMPTTParentModelAdmin,
    PolymorphicMPTTChildModelAdmin,
)
from . import models


def sync_grid_children(modeladmin, request, queryset):
    for grid in queryset.all():
        grid.sync_children()


sync_grid_children.short_description = "Sync grid children nodes"


class BaseSpaceNodeAdmin(PolymorphicMPTTChildModelAdmin):
    GENERAL_FIELDSET = (
        _("General"),
        {
            "fields": ("parent", "name"),
        },
        # _("Dimensions"),
        # {
        #     "fields": ("size", "volume"),
        # }
    )
    list_display = (
        "name",
        "irn",
        "item_count",
    )

    base_model = models.SpaceNode
    # base_readonly_fields = ("parent",)
    base_fieldsets = (GENERAL_FIELDSET,)


class GridSpaceNodeAdmin(BaseSpaceNodeAdmin):
    actions = [
        sync_grid_children,
    ]
    list_display = [
        "name",
        "irn",
        "grid_size",
        "item_count",
    ]


class TreeNodeParentAdmin(PolymorphicMPTTParentModelAdmin):
    # readonly_fields = ("parent",)
    base_model = models.SpaceNode
    child_models = (
        models.SpaceNode,
        models.GridSpaceNode,
    )

    list_display = (
        "name",
        # There appears to be JS that doesn't take into account the extra list items when making the draggable interface
        # "item_count",
        "irn",
        # "actions_column",
    )

    # class Media:
    #     css = {
    #         'all': ('admin/treenode/admin.css',)
    #     }


# admin.site.register(models.SpaceNode, TreeNodeParentAdmin)
admin.site.register(models.SpaceNode, BaseSpaceNodeAdmin)
admin.site.register(models.GridSpaceNode, GridSpaceNodeAdmin)
