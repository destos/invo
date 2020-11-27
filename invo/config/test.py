from .common import Common
from configurations import values


class Test(Common):

    # Change instance urn namespace to test
    INVO_APP_IRN_NAMESPACE = values.Value("test")

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    }
