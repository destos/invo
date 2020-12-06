"""
The spaces app helps create an easy way to divide up physical areas into an organized
hierarchy so as to enable quick lookup and suggested organization.

Spaces can be assigned to different objects that can move into other spaces,
moving the hierarchy with it.

When looking For an item you can request different levels of grids to narrow down where an items may be.
"""

from copy import copy
from decimal import Decimal as D
from functools import reduce
from typing import NamedTuple

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from django_measurement.models import MeasurementField
from measurement.measures import Distance, Volume
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey
from protocol.models import Protocol
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

from .managers import SpaceNodeAllManager, SpaceNodeDeletedManager, SpaceNodeManager


def default_data(*args):
    return dict(layout=None)


def default_size(*args):
    # TODO: see if you can just used Dimensions(1, 1, 1)
    return [Distance("1 m"), Distance("1 m"), Distance("1 m")]


class Dimensions(NamedTuple):
    x: Distance
    y: Distance
    z: Distance


class Layout(NamedTuple):
    x: int
    y: int
    w: int
    h: int


class SpaceNode(Protocol, TimeStampedModel, PolymorphicMPTTModel, SafeDeleteModel):
    """
    A space that items can be organized under
    """

    # TODO: merge the safe delete managers and tree managers

    _safedelete_policy = SOFT_DELETE_CASCADE
    _default_layout = dict(x=0, y=0, w=10, h=10)

    name = models.CharField(_("Name"), max_length=50)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    # TODO: orientation matrix to parent?

    # Physical properties
    # 1km to 1mm
    size = ArrayField(
        MeasurementField(measure=Distance, max_digits=8, decimal_places=4),
        size=3,
        blank=True,
        default=default_size,
    )
    volume = MeasurementField(
        measure=Volume, default=Volume("1", "cubic_m"), max_digits=14, decimal_places=4
    )

    data = models.JSONField(default=default_data, null=False, blank=True)

    objects = SpaceNodeManager()
    objects_all = SpaceNodeAllManager()
    objects_deleted = SpaceNodeDeletedManager()

    class MPTTMeta:
        order_insertion_by = ("name",)

    class Meta:
        ordering = (
            "lft",
            "id",
        )
        unique_together = ("parent", "name")
        verbose_name = _("Space")
        verbose_name_plural = _("Spaces")
        get_latest_by = ("created",)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        # TODO: only update volume when size changes
        self.update_volume()
        # TODO: reset layout when parent changes.
        return super().save(**kwargs)

    @property
    def item_count(self):
        # If there are no descendants of this node, don't do complex count
        if self.get_descendant_count() == 0:
            return self.items.count()
        return self.items.model.objects.in_space(self).count()

    def add_item(self, item):
        return self.items.add(item)

    @property
    def layout(self):
        layout = self.data.get("layout", None)
        return layout if layout is not None else self._default_layout

    @layout.setter
    def layout(self, value):
        layout = self.data.get("layout", None)
        new_layout = copy(self._default_layout)
        if layout is not None:
            new_layout.update(layout)
        new_layout.update(value)
        self.data["layout"] = new_layout
        return new_layout

    @property
    def dimensions(self):
        return Dimensions(*self.size)

    def update_volume(self):
        # Change once we upgrade measures to 4.0
        # This doesn't work
        self.volume = reduce((lambda i, e: i * e), self.size)

    # TODO: when deleting spaces with attached items what should we do?

    # TODO: smart item lookup with left/right bounds in item or space queryset?
    # If you want to query or filter all items that are contained within a parent node
    # Could do a query where all items are searched based on their space left/right value.

    # How to solve space sizing orientation and dimensions

    # TODO: children templating features.


class GridSpaceNode(SpaceNode):
    """
    A type of Space that manages the spaces below it into a grid.
    """

    # Orientation? to other grids
    # How to span nodes? maybe some sort of span config.
    # The total grid size for contained nodes
    grid_size = ArrayField(models.PositiveIntegerField(), size=2, blank=True, null=True)
    # Where in the grid this item is located
    # Maybe this is stored in a json field?
    # position = ArrayField(models.PositiveIntegerField(), size=2, blank=True, null=True)

    # TODO: how to handle spans
    # grid change auto building
    def sync_children(self, child_class=None):
        """Create missing children if needed"""

        if child_class is None:
            child_class = SpaceNode

        assert issubclass(child_class, SpaceNode)

        if self.grid_size is None:
            return

        # Create of update children Spaces
        children = self.get_children()
        deleted_children = self.children.deleted_only()
        remaining = set(children.values_list("id", flat=True))
        active = set()

        x_total, y_total = self.grid_size
        with SpaceNode.objects.delay_mptt_updates():
            for x in range(x_total):
                for y in range(y_total):
                    try:
                        # try to find a previously deleted space to use
                        existing_child = deleted_children.get(data__position=[x, y])
                        self.apply_grid(existing_child)
                        existing_child.undelete()
                        active.add(existing_child.id)
                    except SpaceNode.DoesNotExist:
                        try:
                            # TODO: check deleted children? re-activate?
                            child = children.get(data__position=[x, y])
                        except SpaceNode.DoesNotExist:
                            child = child_class(name=f"{x},{y}", data=dict(position=[x, y]))
                            child.insert_at(self, position="last-child", save=False)
                        finally:
                            self.apply_grid(child)
                            child.save()
                            active.add(child.id)

        # Safe delete the spaces that are orphaned
        children.filter(id__in=(remaining-active)).delete()

    @property
    def grid_basis(self):
        dim = self.dimensions
        # cols_per_unit?
        grid_x, grid_y = self.size
        # TODO: figure out what we need to represent to the grid component
        # need to know how many columns to break the sub spaces into

        # return dict()

    def apply_grid(self, child):
        "Assign grid positional properties to a child"
        pos = child.data.get("position", None)
        if pos is None:
            return
        # No scaling applied for now
        child.layout = Layout(pos[0], pos[1], 1, 1)._asdict()

    class MPTTMeta:
        order_insertion_by = "name"


# class DrawerNode(GridSpaceNode):
# Maybe for parts/tools different drawers for things?
# What extra fields does it add?
# Shelves

# class RackNode(GridSpaceNode):
# Vertical rack with the units marked out. Items can fill multiple units?

# Room
# Wall
# Shelving
# ToolBox
# HardwareBox

# Grid layout templates for common space kinds. ki

# TODO: the concept of a space "home" or items "home", the place where
