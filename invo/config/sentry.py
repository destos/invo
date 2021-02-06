import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from configurations import Configuration, values


class Sentry:
    SENTRY_DSN = values.SecretValue()
    SENTRY_ENVIRONMENT = values.Value("stage")
    SENTRY_SAMPLE_RATE = values.FloatValue(1.0)
    DO_HOSTNAME = values.Value("unset", environ_name="HOSTNAME", environ_prefix="")

    @classmethod
    def post_setup(cls):
        sentry_sdk.init(
            dsn=cls.SENTRY_DSN,
            environment=cls.SENTRY_ENVIRONMENT,
            integrations=[DjangoIntegration(), RedisIntegration()],
            traces_sample_rate=cls.SENTRY_SAMPLE_RATE,
            # If you wish to associate users to errors (assuming you are using
            # django.contrib.auth) you may enable sending PII data.
            send_default_pii=True,
            server_name=cls.DO_HOSTNAME,
        )
