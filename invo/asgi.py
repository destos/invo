"""
ASGI config for invo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from configurations import importer
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "invo.config")
os.environ.setdefault("DJANGO_CONFIGURATION", "Local")

importer.install()

application = get_asgi_application()
