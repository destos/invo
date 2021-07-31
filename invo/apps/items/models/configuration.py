import pghistory
import pgtrigger
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel
from marshmallow import Schema, fields
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

from invo.utils.pghistory import enable_history

from owners.models import SharedSite


@pgtrigger.register(pgtrigger.Protect(name="protect_deletes", operation=(pgtrigger.Delete)))
@enable_history(related_name="declaration_history")
class Declaration(SharedSite, TimeStampedModel, SafeDeleteModel):
    """
    A declaration defines what abilities or configuration an item may have, it should allow you to search/filter
    items by those configurations.

    It does not hold information about a specific configuration.

    Does hold information about compatibilities between different configurations.
    compatibilities?
    could there be declarations that share the same variant option and be deemed compatible?
    Example would be screws.

    Item declarations should be serializeable
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(_("Name"), max_length=50)
    # measurements
    # Differing measurements that use the same name?

    # variants = models.ManyToManyField("Variant")
    # variant restrictions/validation/generators
    # Idea create specific variant combinations that are used for relationships, however validation
    # should be taken into consideration when building them.

    # class Meta:

    template = models.TextField(_("Template"))
    # Use different json fields in the descriptions
    def __str__(self):
        return self.nam

    def add_variant(self, label, name, *variants, conditions=None):
        return Variant.objects.get_or_create(
            name=name, declaration=self, defaults=dict(label=label, options=variants)
        )

    @property
    def tags(self):
        return self.variants.values_list("name", flat=True)

    field_mapping = {}

    @cached_property
    def schema(self):
        defs = dict()
        for v in self.variants.all():
            defs.update({v.name: fields.Str()})
        self.process_schema_defs(defs)
        return Schema.from_dict(defs)

    def process_schema_defs(self, defs):
        pass


# also a shared variant?
class Variant(TimeStampedModel, SafeDeleteModel):
    label = models.CharField(_("Label"), max_length=50)
    name = AutoSlugField(
        _("Name"), populate_from="label", max_length=50, overwrite=False, overwrite_on_add=False
    )
    declaration = models.ForeignKey(
        "Declaration", related_name="variants", on_delete=models.CASCADE
    )
    # Facetted?
    options = ArrayField(models.CharField(max_length=50), blank=True, null=False)

    # assign variant declaration to an item
    items = models.ManyToManyField("items.Item", related_name="variants", through="VariantThrough")

    class Meta:
        unique_together = (("name", "declaration"),)


# class Conditions(TimeStampedModel, SafeDeleteModel):
#     "Validators for different combinations of variants"


# VariantOption?
class VariantThrough(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    item = models.ForeignKey("items.Item", on_delete=models.CASCADE)
    declaration = models.ForeignKey(Declaration, on_delete=models.CASCADE)
    option = models.CharField(max_length=50)


class Configuration(models.Model):
    # Takes a relationship between all variant options and
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        pass


# Need some item taxonomy design.
# How do we want to handle multiple instances or groups of items that are the same thing, but in different locations
# Maybe a silent item where you add an item and if the same name is present, you're given the option to
# Add "another <name of item>" And a new instance is saved that is of that type. Every item has it's own type. Types can be merged?
# When search

__all__ = ["Declaration", "Variant", "Configuration"]
