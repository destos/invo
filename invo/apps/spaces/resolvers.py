from ariadne_extended.resolvers import ModelResolver
from .models import SpaceNode

from graph.types import query
from .types import space_interface


class SpaceNodeResolver(ModelResolver):
    model = SpaceNode
    queryset = SpaceNode.objects.all()


query.set_field("space", SpaceNodeResolver.as_resolver(method="retrieve"))
query.set_field("getSpaces", SpaceNodeResolver.as_resolver(method="list"))


@space_interface.field("children")
def resolve_children(obj, info):
    return obj.children.all()
