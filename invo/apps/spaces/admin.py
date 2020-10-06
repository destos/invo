from django.contrib import admin

from django.utils.translation import ugettext_lazy as _
from polymorphic_tree.admin import PolymorphicMPTTParentModelAdmin, PolymorphicMPTTChildModelAdmin
from . import models

def sync_grid_children(modeladmin, request, queryset):
    for grid in queryset.all():
        grid.sync_children()

sync_grid_children.short_description = "Sync grid children nodes"


class BaseSpaceNodeAdmin(PolymorphicMPTTChildModelAdmin):
    # readonly_fields = ("parent",)
    GENERAL_FIELDSET = (None, {
        'fields': ("parent", 'name'),
    })

    base_model = models.SpaceNode
    base_fieldsets = (
        GENERAL_FIELDSET,
    )


class GridSpaceNodeAdmin(BaseSpaceNodeAdmin):
    actions = [sync_grid_children,]


class TreeNodeParentAdmin(PolymorphicMPTTParentModelAdmin):
    base_model = models.SpaceNode
    child_models = (models.SpaceNode, models.GridSpaceNode,)

    list_display = ('name', 'actions_column', )


admin.site.register(models.SpaceNode, TreeNodeParentAdmin)
admin.site.register(models.GridSpaceNode, GridSpaceNodeAdmin)
