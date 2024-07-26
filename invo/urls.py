from django.apps import apps
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("admin/", admin.site.urls),
    path("prot/", include("protocol.urls")),
    path("items/", include("items.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]

if apps.is_installed("django_browser_reload"):
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
if apps.is_installed("debug_toolbar"):
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
if apps.is_installed("pattern_library"):
    urlpatterns += [path("patterns/", include("pattern_library.urls"))]
