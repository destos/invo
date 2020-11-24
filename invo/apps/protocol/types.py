from ariadne import InterfaceType, ScalarType
from ariadne_extended.cursor_pagination.types import resolve_node_type


from .models import IRN


irn_scalar = ScalarType("IRN")
protocol_interface = InterfaceType("Protocol")


@irn_scalar.serializer
def serialize_irn(value):
    "Turn an IRN into a serialized value"
    if isinstance(value, IRN):
        return str(value)
    elif isinstance(value, str):
        return str(IRN.parse(value))
    raise ValueError("how'd you get here?")


@irn_scalar.value_parser
def parse_irn(value):
    return IRN.parse(value)


protocol_interface.set_type_resolver(resolve_node_type)
