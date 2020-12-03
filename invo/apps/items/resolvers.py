from ariadne_extended.resolvers import ModelResolver
from ariadne_extended.cursor_pagination import RelayModelMixin
from . import models
from . import serializers

from graph.types import query, mutation
from .types import item_interface


class ItemResolver(RelayModelMixin, ModelResolver):
    model = models.Item
    queryset = models.Item.objects.all()

    type_serializers = {
        models.Item: serializers.ItemSerializer,
        models.Tool: serializers.ToolSerializer,
        models.Consumable: serializers.ConsumableSerializer,
    }

    def get_serializer_class(self):
        model = self.config.get("model", models.Item)
        return self.type_serializers[model]

    def perform_destroy(self, instance):
        # FIX: in extended, graphql.error.graphql_error.GraphQLError: cannot unpack non-iterable NoneType object
        return 1, instance.delete()


# TODO: just use space.parents
@item_interface.field("spaceParents")
def resolve_space_parents(item, info, **kwargs):
    depth = kwargs.get("depth", 100)
    if item.space:
        return item.space.get_ancestors(include_self=True)[:depth]
    return []


query.set_field("item", ItemResolver.as_resolver(method="retrieve"))
query.set_field("items", ItemResolver.as_resolver(method="list"))

mutation.set_field("addItem", ItemResolver.as_resolver(method="create"))
mutation.set_field("addTool", ItemResolver.as_resolver(method="create", model=models.Tool))
mutation.set_field(
    "addConsumable", ItemResolver.as_resolver(method="create", model=models.Consumable)
)
mutation.set_field("updateItem", ItemResolver.as_resolver(method="update"))
mutation.set_field("updateTool", ItemResolver.as_resolver(method="update", model=models.Tool))
mutation.set_field(
    "updateConsumable", ItemResolver.as_resolver(method="update", model=models.Consumable)
)

mutation.set_field("deleteItem", ItemResolver.as_resolver(method="destroy"))
# TODO: moveItem, removeItem, putBackItem
