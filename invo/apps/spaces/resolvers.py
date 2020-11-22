from ariadne_extended.resolvers import ModelResolver, ListModelMixin
from .models import SpaceNode

from graph.types import query
from .types import space_interface, grid_space_node
from .filters import SpaceNodeFilter
from items.resolvers import ItemResolver


class SpaceNodeResolver(ListModelMixin, ModelResolver):
    model = SpaceNode
    filterset_class = SpaceNodeFilter
    queryset = SpaceNode.objects.all()


grid_space_node.set_alias("size", "grid_size")


query.set_field("space", SpaceNodeResolver.as_resolver(method="retrieve"))
query.set_field("getSpaces", SpaceNodeResolver.as_resolver(method="list"))

space_interface.set_field("children", SpaceNodeResolver.as_nested_resolver(method="list"))
space_interface.set_field("items", ItemResolver.as_nested_resolver(method="list"))
