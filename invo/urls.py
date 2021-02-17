from ariadne.contrib.django.views import GraphQLView, MiddlewareManager
from graph.middleware import JWTMiddleware
from django.contrib import admin
from django.urls import path
from graph.schema import schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# TODO: using cookies for tokens is more secure. Investigate
# from graph.views import CookieTokenObtainPairView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        GraphQLView.as_view(
            schema=schema,
            middleware=MiddlewareManager(JWTMiddleware())
            # playground_options={
            #     "endpoint": "dev-graphql?headers={}".format(
            #         json.dumps({"Authorization": f"Token {token}"})
            #     )
            # },
        ),
        name="dev-graphql",
    ),
    # path("token/", CookieTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
