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

    @property
    def MIDDLEWARE(self):
        # insert whitenoise after django security middleware
        mw = list(copy(Common.MIDDLEWARE))
        mw.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
        return mw

    # whitenoise
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    WHITENOISE_MANIFEST_STRICT = False

    USE_X_FORWARDED_HOST = True
    FORCE_SCRIPT_NAME = "/api"

    # INVO APP SETTINGS
    INVO_APP_IRN_NAMESPACE = values.Value("prod")
