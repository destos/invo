# -*- coding: utf-8 -*-
"""
Production Configurations
- Debug mode never on
- Uses console backend for emails
"""

from configurations import values

from .common import Common


class Prod(Common):

    # DEBUG
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    # END DEBUG

    CORS_ALLOW_CREDENTIALS = True

    INVO_APP_IRN_NAMESPACE = values.Value("prod")
