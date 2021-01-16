from ariadne import EnumType, InterfaceType, ObjectType, UnionType
from ariadne_extended.cursor_pagination.types import resolve_node_type

space_node = ObjectType("SpaceNode")
grid_space_node = ObjectType("GridSpaceNode")
space_interface = InterfaceType("SpaceInterface")

space = UnionType("SpaceTypes", type_resolver=resolve_node_type)
