from ariadne_extended.views import BaseGraphQLView  # type: ignore
from django.contrib import admin
from django.urls import path
from graph.schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        BaseGraphQLView.as_view(
            schema=schema,
            # playground_options={
            #     "endpoint": "dev-graphql?headers={}".format(
            #         json.dumps({"Authorization": f"Token {token}"})
            #     )
            # },
        ),
        name="dev-graphql",
    ),
]
