from ariadne_extended.resolvers import ListModelMixin, ModelResolver
from graph.types import mutation, query
from items.resolvers import ItemResolver

from .filters import SpaceNodeFilter
from .models import SpaceNode, GridSpaceNode
from .serializers import SpaceNodeSerializer, GridSpaceNodeSerializer
from .types import grid_space_node, space_interface


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


class GridSpaceNodeResolver(SpaceNodeResolver):
    model = GridSpaceNode
    serializer_class = GridSpaceNodeSerializer
    queryset = GridSpaceNode.objects.all()


grid_space_node.set_field("gridSize", lambda g, i: dict(cols=g.grid_size[0], rows=g.grid_size[1]))

query.set_field("space", SpaceNodeResolver.as_resolver(method="retrieve"))
query.set_field("getSpaces", SpaceNodeResolver.as_resolver(method="list"))

mutation.set_field("addSpace", SpaceNodeResolver.as_resolver(method="create"))
mutation.set_field("addGridSpace", GridSpaceNodeResolver.as_resolver(method="create"))
mutation.set_field("updateSpaceLayout", SpaceNodeResolver.as_resolver(method="update_layout"))
mutation.set_field("updateSpace", SpaceNodeResolver.as_resolver(method="update"))
mutation.set_field("updateGridSpace", GridSpaceNodeResolver.as_resolver(method="update"))
mutation.set_field("removeSpace", SpaceNodeResolver.as_resolver(method="destroy"))

space_interface.set_field("children", SpaceNodeResolver.as_nested_resolver(method="list"))
# TODO: distinguishing and querying direct children and all child items on space via field arg?
space_interface.set_field("items", ItemResolver.as_nested_resolver(method="list"))
space_interface.set_field("isLeaf", lambda m, i: m.is_leaf_node())
space_interface.set_field("isChild", lambda m, i: m.is_child_node())
space_interface.set_field("isRoot", lambda m, i: m.is_root_node())


@space_interface.field("parents")
def resolve_ancestors(space, info, **kwargs):
    return space.get_ancestors(ascending=False, include_self=False).all()
