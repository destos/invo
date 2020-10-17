from ariadne_extended.resolvers import ModelResolver
from ariadne_extended.cursor_pagination import RelayModelMixin
from .models import Item

from graph.types import query


class ItemResolver(RelayModelMixin, ModelResolver):
    model = Item
    queryset = Item.objects.all()


query.set_field("item", ItemResolver.as_resolver(method="retrieve"))
query.set_field("items", ItemResolver.as_resolver(method="list"))
