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


class Ngrok(Sentry, Common):

    # DEBUG
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    # END DEBUG

    CORS_ALLOW_CREDENTIALS = True
    # origin list isn't working...
    CORS_ORIGIN_WHITELIST = ["https://myinvo.ngrok.io"]
    CORS_ORIGIN_ALLOWS_ALL = True

    @property
    def MIDDLEWARE(self):
        # insert whitenoise after django security middleware
        mw = list(copy(Common.MIDDLEWARE))
        mw.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
        return mw

    # whitenoise
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    WHITENOISE_MANIFEST_STRICT = False
    STATIC_URL = "static/"

    USE_X_FORWARDED_HOST = True
    # FORCE_SCRIPT_NAME = "/api/"

    # INVO APP SETTINGS
    INVO_APP_IRN_NAMESPACE = values.Value("ngrok")
