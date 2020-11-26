from ariadne import MutationType, QueryType, ObjectType

query = QueryType()

mutation = MutationType()

# Built in django type mapping
user = ObjectType("User")
group = ObjectType("Group")
permission = ObjectType("Permission")
