from django.contrib import admin
from safedelete.admin import SafeDeleteAdmin, highlight_deleted

from . import models


@admin.register(models.Situation)
class SituationAdmin(SafeDeleteAdmin):
    list_display = (
        highlight_deleted,
        "user",
        "space",
        "item",
        "created",
        "modified",
    ) + SafeDeleteAdmin.list_display
    list_filter = SafeDeleteAdmin.list_filter
    date_hierarchy = "created"
    raw_id_fields = ("user", "space", "item")
