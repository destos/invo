from ariadne_extended.cursor_pagination import RelayModelMixin
from ariadne_extended.resolvers import ModelResolver
from graph.types import mutation, query

from . import models, serializers
from .types import item_interface
from owners.resolvers import OwnerResolverMixin


class ItemResolver(OwnerResolverMixin, RelayModelMixin, ModelResolver):
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
        # FIX: in ariadne extended, graphql.error.graphql_error.GraphQLError: cannot unpack non-iterable NoneType object
        return (1, instance.delete())

    def filter_nested_queryset(self, queryset):
        if self.operation_kwargs.get("childItems", False):
            return super().filter_nested_queryset(queryset)
        return queryset.in_space(self.parent)


# TODO: just use space.parents
@item_interface.field("spaceParents")
def resolve_space_parents(item, info, **kwargs):
    depth = kwargs.get("depth", 100)
    if item.space:
        return item.space.get_ancestors(include_self=True)[:depth]
    return []


def resolve_suggest_type(parent, info, **kwargs):
    return "ITEM"


query.set_field("item", ItemResolver.as_resolver(method="retrieve"))
query.set_field("items", ItemResolver.as_resolver(method="list"))
query.set_field("suggestType", resolve_suggest_type)

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
