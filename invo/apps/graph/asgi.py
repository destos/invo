from ariadne.asgi import GraphQL
from .schema import schema

application = GraphQL(schema)
