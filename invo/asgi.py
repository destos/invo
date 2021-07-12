"""
ASGI config for invo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from configurations import importer

# from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path, path
from django.core.asgi import get_asgi_application
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "invo.config")
os.environ.setdefault("DJANGO_CONFIGURATION", "Local")

importer.install()
# Get asi application must come before further imports to prevent django model ready errors.
django_asgi_app = get_asgi_application()

from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from graph.asgi import application as graph_application

router = ProtocolTypeRouter(
    {
        "websocket": URLRouter([re_path(r"^ws/$", graph_application)]),
        "http": django_asgi_app,
    }
)

# application = django_asgi_app
application = SentryAsgiMiddleware(router)
