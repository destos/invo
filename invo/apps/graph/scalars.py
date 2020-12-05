# from .types import distance_scalar
from decimal import Decimal
from measurement.measures import Distance

# measures scalars

# @distance_scalar.serializer
def serialize_distance(value):
    return dict(
        value=float(value.si_value),
        unit=value.unit.name
    )

# @distance_scalar.value_parser
def parse_distance(value):
    return Distance(**{value["unit"]: Decimal(value["value"])})
