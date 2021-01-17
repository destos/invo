from ariadne import MutationType, ObjectType, QueryType, ScalarType

from .scalars import parse_distance, parse_volume, serialize_measure

query = QueryType()

mutation = MutationType()

distance_scalar = ScalarType("Distance", serializer=serialize_measure, value_parser=parse_distance)
volume_scalar = ScalarType("Volume", serializer=serialize_measure, value_parser=parse_volume)
