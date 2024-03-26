from django.contrib import admin
from django.urls import path
from django.urls.conf import include

# from graph.middleware import JWTMiddleware
# from graph.schema import schema

# TODO: using cookies for tokens is more secure. Investigate
# from graph.views import CookieTokenObtainPairView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("prot/", include("protocol.urls")),
]
