from ariadne import make_executable_schema, snake_case_fallback_resolvers
from ariadne.contrib.django.scalars import date_scalar, datetime_scalar
from django.apps import apps

config = apps.get_app_config("graph_loader")


schema = make_executable_schema(
    config.type_defs,
    config.all_app_types + [snake_case_fallback_resolvers, datetime_scalar, date_scalar],
)
