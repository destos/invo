from ariadne_extended.resolvers import ModelResolver, ListModelMixin
from .models import SpaceNode

from graph.types import query
from .types import space_interface
from .filters import SpaceNodeFilter


class SpaceNodeResolver(ListModelMixin, ModelResolver):
    model = SpaceNode
    filterset_class = SpaceNodeFilter
    queryset = SpaceNode.objects.all()


query.set_field("space", SpaceNodeResolver.as_resolver(method="retrieve"))
query.set_field("getSpaces", SpaceNodeResolver.as_resolver(method="list"))

space_interface.set_field("children", SpaceNodeResolver.as_nested_resolver(method="list"))
