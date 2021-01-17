from ariadne import MutationType, ObjectType, QueryType, ScalarType

# Built in django type mapping
user = ObjectType("User")
group = ObjectType("Group")
permission = ObjectType("Permission")
