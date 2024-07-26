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
    INTERNAL_IPS = [
        "127.0.0.1",
    ]

    CORS_ALLOW_CREDENTIALS = True

    INVO_APP_IRN_NAMESPACE = values.Value("local")

    ALLOWED_HOSTS = ["*"]

    PATTERN_LIBRARY = {
        # Groups of templates for the pattern library navigation. The keys
        # are the group titles and the values are lists of template name prefixes that will
        # be searched to populate the groups.
        "SECTIONS": (
            ("components", ["patterns/components"]),
            ("pages", ["patterns/pages"]),
        ),
        # Configure which files to detect as templates.
        "TEMPLATE_SUFFIX": ".html",
        # Set which template components should be rendered inside of,
        # so they may use page-level component dependencies like CSS.
        "PATTERN_BASE_TEMPLATE_NAME": "patterns/base.html",
        # Any template in BASE_TEMPLATE_NAMES or any template that extends a template in
        # BASE_TEMPLATE_NAMES is a "page" and will be rendered as-is without being wrapped.
        "BASE_TEMPLATE_NAMES": ["patterns/base_page.html"],
    }
