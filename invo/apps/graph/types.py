from ariadne import MutationType, QueryType, ObjectType, ScalarType
from .scalars import serialize_measure, parse_distance, parse_volume

query = QueryType()

mutation = MutationType()

# Built in django type mapping
user = ObjectType("User")
group = ObjectType("Group")
permission = ObjectType("Permission")

distance_scalar = ScalarType("Distance", serializer=serialize_measure, value_parser=parse_distance)
volume_scalar = ScalarType("Volume", serializer=serialize_measure, value_parser=parse_volume)
