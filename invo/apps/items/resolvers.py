from ariadne_extended.resolvers import ModelResolver
from ariadne_extended.cursor_pagination import RelayModelMixin
from .models import Item

from graph.types import query
from .types import item_interface


class ItemResolver(RelayModelMixin, ModelResolver):
    model = Item
    queryset = Item.objects.all()


@item_interface.field("spaceParents")
def resolve_space_parents(item, info, **kwargs):
    depth = kwargs.get("depth", 100)
    if item.space:
        return item.space.get_ancestors(include_self=True)[:depth]
    return []


query.set_field("item", ItemResolver.as_resolver(method="retrieve"))
query.set_field("items", ItemResolver.as_resolver(method="list"))
