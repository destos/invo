"""
The spaces app helps create an easy way to divide up physical areas into an organized
hierarchy so as to enable quick lookup and suggested organization.

Spaces can be assigned to different objects that can move into other spaces,
moving the hierarchy with it.

When looking For an item you can request different levels of grids to narrow down where an items may be.
"""

from copy import deepcopy
from decimal import Decimal as D
from functools import reduce
from typing import NamedTuple, Union

import glom
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from django_measurement.models import MeasurementField
from measurement.measures import Distance, Volume
from model_utils import FieldTracker
from mptt.fields import TreeForeignKey
from owners.models import SingularSite
from polymorphic_tree.models import PolymorphicMPTTModel
from protocol.models import Protocol
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

from .layouts import Layout
from .managers import (
    CurrentSiteSpaceNodeManager,
    SpaceNodeAllManager,
    SpaceNodeDeletedManager,
    SpaceNodeManager,
)


def default_data(*args):
    return dict()


def default_size(*args):
    # TODO: see if you can just used Dimensions(1, 1, 1)
    return [Distance("1 m"), Distance("1 m"), Distance("1 m")]


def merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value

    return destination


class Dimensions(NamedTuple):
    x: Distance
    y: Distance
    z: Distance


class SpaceNode(SingularSite, Protocol, TimeStampedModel, PolymorphicMPTTModel, SafeDeleteModel):
    """
    A space that items can be organized under.

    Areas of concern:
    * Own dimensions
    * Child dimension validity
    * If containing children, grid sizing options
    orientation
    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    _default_layout = dict(x=0, y=0, w=10, h=10)

    name = models.CharField(_("Name"), max_length=50)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    # TODO: orientation matrix to parent?
    # TODO: child spaces should not have dimensions larger than the parent, make sure orientation is taken into account
    # TODO: child spaces should have properties that show the max allowed size of the child based on parent or parent grid settings?

    # Physical properties
    # 1km to 1mm
    # max size doesn't seem to be the restriction max digits provides
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

    # Grid properties
    grid_scale = MeasurementField(
        measure=Distance,
        default=Distance("1", "cm"),
        max_digits=14,
        decimal_places=4,
        null=True,
        blank=True,
    )
    # For viewing sub spaces in the correct orientation if doing validation calculations
    # grid_orientation =

    tracker = FieldTracker(fields=["grid_scale", "size"])

    objects = SpaceNodeManager()
    objects_all = SpaceNodeAllManager()
    objects_deleted = SpaceNodeDeletedManager()
    # Current site objects are only non-deleted spaces
    current_site_objects = CurrentSiteSpaceNodeManager()

    def update_data(self, **data):
        """Update that data yo, and do it nicely, doesn't handle removing data easily"""
        defaults = data.pop("defaults", None)
        orig_data = deepcopy(self.data)
        data = deepcopy(data)

        if defaults is not None:
            defaults = deepcopy(defaults)
            data = merge(data, defaults)

        data = merge(data, orig_data)
        self.data = data
        return self.data

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
        # only update volume when size changes
        if self.tracker.has_changed("size"):
            self.update_volume()

        # Update the child layout if size changes or grid scale changes
        if self.tracker.has_changed("grid_scale") or self.tracker.has_changed("size"):
            previous = self.tracker.changed()
            # Should we pass in a changed/delta object to use when adjusting sizes
            # How to handle remainders in calculations? only allow clean calculations?
            self.update_child_layout(previous)

        return super().save(**kwargs)

    @property
    def item_count(self):
        # If there are no descendants of this node, don't do complex count
        if self.get_descendant_count() == 0:
            return self.items.count()
        return self.items.model.objects.in_space(self).count()

    def add_item(self, item):
        return self.items.add(item)

    # Grid positioning
    @property
    def layout(self):
        layout = self.data.get("layout", None)
        # TODO: layout in data should always be dict, check?
        # Always return a layout named tuple
        return Layout(**layout) if layout is not None else Layout(**self._default_layout)

    @layout.setter
    def layout(self, layout: Union[Layout, dict]):
        # Always set data as a dict
        if isinstance(layout, Layout):
            layout = layout._asdict()
        self.update_data(layout=layout, defaults=(dict(layout=self._default_layout)))
        return self.data["layout"]

    def update_volume(self):
        # Change once we upgrade measures to 4.0
        # This doesn't work
        self.volume = reduce((lambda i, e: i * e), self.size)

    @property
    def dimensions(self):
        """Dimensions object for working with space size"""
        return Dimensions(*self.size)

    # Child grid helpers
    @property
    def grid_config(self):
        "Configuration to use in grid component for space display"
        cols, rows = self.grid_basis
        return dict(cols=int(cols), row_basis=rows / cols)

    @property
    def grid_basis(self):
        """Ratio of units to grid sizes and errors related to that?"""
        return self.calculate_grid_basis(self.dimensions, self.grid_scale)

    @classmethod
    def calculate_grid_basis(cls, dimensions, scale):
        width = dimensions.x
        height = dimensions.y
        # rem = Decimal(width) % Decimal(scale)
        # assert rem == 0
        return width / scale, height / scale

    def update_child_layout(self, previous):
        old_scale = previous.get("grid_scale", self.grid_scale)
        size = previous.get("size", self.size)
        if old_scale is None or size is None:
            return
        old_dimensions = Dimensions(*size)
        old_basis, _ = self.calculate_grid_basis(old_dimensions, old_scale)
        new_basis = self.grid_basis
        delta = D(old_basis / new_basis[0])
        for child in self.children.all():
            child.scale_layout(delta)
            child.save(update_fields=("data",))

    def scale_layout(self, delta):
        self.layout = self.layout / delta

    """
    TODO: when deleting spaces with attached items what should we do?
    Maybe There should be a delete validity check, similar to django admin with related objects.
    Give the option to move them to a specific place

    TODO: smart item lookup with left/right bounds in item or space queryset?
    If you want to query or filter all items that are contained within a parent node
    Could do a query where all items are searched based on their space left/right value.

    How to solve space sizing orientation and dimensions

    TODO: children templating features.
    templating is not a grid, but the outcome is saved grid positioning that can scale
    """


class GridSpaceNode(SpaceNode):
    """
    A type of Space that manages the spaces below it into a grid.
    """

    # TODO: rename to something like strict grid space? as it organizes all children into a strict grid for you automatically

    # Orientation? to other grids
    # How to span nodes? maybe some sort of span config.
    # The total grid size for contained nodes
    # Column/Rows
    grid_size = ArrayField(models.PositiveIntegerField(), size=2, blank=True, null=True)
    # Where in the grid this item is located
    # Maybe this is stored in a json field?
    # position = ArrayField(models.PositiveIntegerField(), size=2, blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = "name"

    def save(self, sync_children=True, **kwargs):
        # Get state before save
        adding = self._state.adding
        super().save(**kwargs)
        if sync_children and adding:
            self.sync_children()

    # TODO: how to handle spans
    # grid change auto building
    def sync_children(self, child_class=None):
        """Create missing children if needed"""
        # TODO: should it be aware of where items were assigned previously are move them back?
        # TODO: should be able to pass the size based on the parent size to the child. When parent changes, children should be updated

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

        col_total, row_total = self.grid_size
        with SpaceNode.objects.delay_mptt_updates():
            for col in range(col_total):
                for row in range(row_total):
                    try:
                        # try to find a previously deleted space to re-use
                        existing_child = deleted_children.get(data__position=[col, row])
                        self.apply_grid(existing_child)
                        existing_child.undelete()
                        active.add(existing_child.id)
                    except SpaceNode.DoesNotExist:
                        try:
                            # TODO: check deleted children? re-activate?
                            child = children.get(data__position=[col, row])
                        except SpaceNode.DoesNotExist:
                            child = child_class(
                                name=f"{col},{row}", data=dict(position=[col, row]), site=self.site
                            )
                            child.insert_at(self, position="last-child", save=False)
                        finally:
                            self.apply_grid(child)
                            child.save()
                            active.add(child.id)

        # Safe delete the spaces that are orphaned
        children.filter(id__in=(remaining - active)).delete()

    @property
    def grid_basis(self):
        """
        Find the multipliers needed to position a child grid space based on the desired grid scale
        Take the total size of the grid space and the desired grid size and create the ratio needed to divide

        OK, so I'm trying to make a system that is conflicting. I can either specify how many segments I want the grid.
        Or, I can specify some desired fractional dimension based on the full width/height of the object or organizational area.
        Can't have it both ways.

        What is the usecase for either. Do I make it selectable. You specify the grid size,
        This model class is meant to help with easily creating a grid of sub-child spaces. Maybe this isn't the place for it
        """
        # dim = self.dimensions
        # dim.x
        # dim.y
        # Apply orientation transform?

        # cols_per_unit?
        # grid_rows, grid_cols = self.grid_size
        return self.grid_size
        # TODO: figure out what we need to represent to the grid component
        # need to know how many columns to break the sub spaces into

        # return dict()

    def child_inside(self, child):
        """
        determine if a child is inside the dimensions of the grid space.
        """
        pass

    def apply_grid(self, child):
        "Assign grid positional properties to a child"
        pos = child.data.get("position", None)
        if pos is None:
            return
        # No scaling applied for now
        child.layout = Layout(pos[0], pos[1], 1, 1)

    # @property
    # def grid_config(self):
    #     cols, rows = self.grid_basis
    #     "Configuration to use in grid component for grid space display"
    #     # TODO: row height calculated from grid size and dimension ratio via basis?
    #     return dict(cols=cols, row_basis=rows / y)


# templates = dict(home_depo_shelve=dict(grid_size=[1, 6]))

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
