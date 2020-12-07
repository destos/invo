from ariadne_extended.resolvers import ModelResolver, ListModelMixin
from .models import SpaceNode

from graph.types import mutation, query
from .types import space_interface, grid_space_node
from .filters import SpaceNodeFilter
from items.resolvers import ItemResolver
from .serializers import SpaceNodeSerializer


class SpaceNodeResolver(ListModelMixin, ModelResolver):
    model = SpaceNode
    filterset_class = SpaceNodeFilter
    serializer_class = SpaceNodeSerializer
    queryset = SpaceNode.objects.all()

    def update_layout(self, info, layout=None, **kwargs):
        space = self.get_object()
        setattr(space, "layout", layout)
        space.save()
        return space


# grid_space_node.set_alias("size", "grid_size")

query.set_field("space", SpaceNodeResolver.as_resolver(method="retrieve"))
query.set_field("getSpaces", SpaceNodeResolver.as_resolver(method="list"))

mutation.set_field("addSpace", SpaceNodeResolver.as_resolver(method="create"))
mutation.set_field("updateSpaceLayout", SpaceNodeResolver.as_resolver(method="update_layout"))
mutation.set_field("updateSpace", SpaceNodeResolver.as_resolver(method="update"))
mutation.set_field("removeSpace", SpaceNodeResolver.as_resolver(method="destroy"))

space_interface.set_field("children", SpaceNodeResolver.as_nested_resolver(method="list"))
# TODO: distinquishing and quering direct and all child items on space
space_interface.set_field("items", ItemResolver.as_nested_resolver(method="list"))


@space_interface.field("parents")
def resolve_ancestors(space, info, **kwargs):
    return space.get_ancestors(ascending=False, include_self=False).all()
