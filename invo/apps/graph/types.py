from ariadne import MutationType, QueryType, ObjectType, ScalarType
from .scalars import serialize_distance, parse_distance

query = QueryType()

mutation = MutationType()

# Built in django type mapping
user = ObjectType("User")
group = ObjectType("Group")
permission = ObjectType("Permission")

distance_scalar = ScalarType("Distance", serializer=serialize_distance, value_parser=parse_distance)
