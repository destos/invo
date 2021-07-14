from configurations import values

from .common import Common


class Build(Common):

    # Change instance urn namespace to build
    INVO_APP_IRN_NAMESPACE = values.Value("build")

    HAYSTACK_CONNECTIONS = {
        "default": {
            "ENGINE": "haystack.backends.simple_backend.SimpleEngine",
        },
    }

    # whitenoise
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
