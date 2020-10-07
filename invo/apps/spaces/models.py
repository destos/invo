"""
The spaces app help create an easy way to divide up physical areas into an organized
hierarchy so as to enable quick lookup and suggested organization.

Spaces can be assigned to different objects that can move into other spaces,
moving the hierarchy with it.

When looking For an item you can request different levels of grids to narrow down where an items may be.
"""

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey

from invo.utils.protocol import Protocol


class SpaceNode(Protocol, TimeStampedModel, PolymorphicMPTTModel):
    """
    A space that objects can be organized under
    """
    name = models.CharField(_("Name"), max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    data = models.JSONField(null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ('name',)
    
    class Meta:
        ordering = ('parent__name', 'name')
        unique_together = ('parent', 'name')
        verbose_name = _('Space')
        verbose_name_plural = _('Spaces')

    def __str__(self):
        return self.name
    
    # TODO: smart item lookup with left/right bounds in item or space queryset?
    # If you want to query or filter all items that are contained within a parent node
    # Could do a query where all items are searched based on their space left/right value.


class GridSpaceNode(SpaceNode):
    """
    A type of Space that manages the spaces below it into a grid,
    A Grid can be terminated,
    
    How to span nodes
    """
    # The total grid size for contained nodes
    grid_size = ArrayField(models.PositiveIntegerField(), size=2, blank=True, null=True)
    # Where in the grid this item is located
    # Maybe this is stored in a json field?
    # position = ArrayField(models.PositiveIntegerField(), size=2, blank=True, null=True)

    # Whether or not further grid children can be assigned
    # irreducible = models.BooleanField(_("Irreducible"), default=False)

    # TOOD: how to handle spans
    # grid change auto building
    def sync_children(self, child_class=None):
        """Create missing children if needed"""

        if child_class is None:
            child_class = GridSpaceNode

        assert issubclass(child_class, SpaceNode)

        if self.grid_size is None:
            return

        # Create of update children Spaces
        children = self.get_children()

        x_total, y_total = self.grid_size
        with SpaceNode.objects.delay_mptt_updates():
            for x in range(x_total):
                for y in range(y_total):
                    if not children.instance_of(GridSpaceNode).filter(data__position=[x, y]).exists():
                        child_class(name=f"{x},{y}", data=dict(position=[x, y])).insert_at(self, position="last-child", save=True)

    def add_item(self, item):
        return self.items.add(item)

    class MPTTMeta:
        order_insertion_by = ("name")


# class DrawerNode(GridSpaceNode):
# Maybe for parts/tools different drawers for things?
# What extra fields does it add?

# class RackNode(GridSpaceNode):
# Vertical rack with the units marked out. Items can fill multiple units?