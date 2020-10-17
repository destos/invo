from ariadne import EnumType, ObjectType, UnionType, InterfaceType
from ariadne_extended.cursor_pagination.types import resolve_node_type

item = ObjectType("Item")
tool = ObjectType("Tool")
consumable = ObjectType("Consumable")
tracked_consumable = ObjectType("TrackedConsumable")

item_interface = InterfaceType("ItemInterface")
consumable_interface = InterfaceType("ConsumableInterface")

item_types_union = UnionType("ItemTypes", type_resolver=resolve_node_type)
