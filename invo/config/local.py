# -*- coding: utf-8 -*-
"""
Local Configurations
- Runs in Debug mode
- Uses console backend for emails
"""

from configurations import values

from .common import Common


class Local(Common):

    # DEBUG
    DEBUG = values.BooleanValue(True)
    TEMPLATE_DEBUG = DEBUG
    # END DEBUG

    # INSTALLED_APPS
    # INSTALLED_APPS = Common.INSTALLED_APPS
    # END INSTALLED_APPS

    # Mail settings
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_BACKEND = values.Value("django.core.mail.backends.console.EmailBackend")
    # End mail settings

    CORS_ALLOWED_ORIGINS = [
        "http://localhost:8000",
        "http://localhost:3000",
        "http://127.0.0.1:8000",
    ]

    CORS_ALLOW_CREDENTIALS = True

    INVO_APP_IRN_NAMESPACE = values.Value("local")
