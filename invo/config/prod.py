# -*- coding: utf-8 -*-
"""
Production Configurations
- Debug mode never on
- Meant to be served from digital ocean
"""
from copy import copy

from configurations import values

from .common import Common
from .sentry import Sentry


class Prod(Sentry, Common):

    # DEBUG
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    # END DEBUG

    CORS_ALLOW_CREDENTIALS = True

    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    # Don't redirect to ssl as DO handles SSL layer
    SECURE_SSL_REDIRECT = False

    @property
    def MIDDLEWARE(self):
        # insert whitenoise after django security middleware
        mw = list(copy(Common.MIDDLEWARE))
        mw.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
        return mw

    # server
    USE_X_FORWARDED_HOST = True
    FORCE_SCRIPT_NAME = "/api"

    # whitenoise
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    WHITENOISE_MANIFEST_STRICT = False
    STATIC_URL = FORCE_SCRIPT_NAME + Common.STATIC_URL

    # INVO APP SETTINGS
    INVO_APP_IRN_NAMESPACE = values.Value("prod")
