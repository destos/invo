# -*- coding: utf-8 -*-
"""
Django settings for invo project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import join
from pathlib import Path
import sys

from configurations import Configuration, values
import dj_search_url

dj_search_url.SCHEMES["elasticsearch"] = "haystack.backends.elasticsearch5_backend.Elasticsearch5SearchEngine"

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(join(BASE_DIR, "apps"))



class Common(Configuration):

    BASE_DIR = BASE_DIR

    # SECRET CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
    # Note: This key only used for development and testing.
    #       In production, this is changed to a values.SecretValue() setting
    SECRET_KEY = values.SecretValue()
    # END SECRET CONFIGURATION

    # DEBUG
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
    TEMPLATE_DEBUG = DEBUG
    # END DEBUG

    # APP CONFIGURATION
    DJANGO_APPS = (
        "django.contrib.admin",
        "django.contrib.auth",
        "polymorphic_tree",
        "polymorphic",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    )

    THIRD_PARTY_APPS = (
        "django_extensions",
        "safedelete",
        "mptt",
        "waffle",
        "corsheaders",
        "qr_code",
        "ariadne.contrib.django",
        "ariadne_extended.graph_loader",
        "ariadne_extended.cursor_pagination",
        # "ariadne_extended.payload",
        "ariadne_extended.contrib.waffle_graph",
        "haystack",
    )

    LOCAL_APPS = (
        "situations",
        "protocol",
        "graph",
        "spaces",
        "items",
        "entity_search",
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
    # END APP CONFIGURATION

    # MIDDLEWARE CONFIGURATION
    MIDDLEWARE = (
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    )
    # END MIDDLEWARE CONFIGURATION

    # EMAIL CONFIGURATION
    EMAIL_BACKEND = values.Value("django.core.mail.backends.smtp.EmailBackend")
    # END EMAIL CONFIGURATION

    # MANAGER CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
    ADMINS = values.SingleNestedTupleValue()

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
    # MANAGERS = values.SingleNestedTupleValue()
    # END MANAGER CONFIGURATION

    # DATABASE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
    DATABASES = values.DatabaseURLValue("postgres://localhost/invo")
    # END DATABASE CONFIGURATION

    # CACHING
    # Do this here because thanks to django-pylibmc-sasl and pylibmc
    # memcacheify (used on heroku) is painful to install on windows.
    CACHES = {
        "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": ""}
    }
    # END CACHING

    # GENERAL CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
    TIME_ZONE = "America/Chicago"

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
    LANGUAGE_CODE = "en-us"

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
    SITE_ID = 1

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
    USE_I18N = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
    USE_L10N = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
    USE_TZ = True
    # END GENERAL CONFIGURATION

    # TEMPLATE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    # STATIC FILE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
    # STATIC_ROOT = join(os.path.dirname(BASE_DIR), 'staticfiles')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    STATIC_URL = "/static/"

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
    # STATICFILES_DIRS = (
    #     join(BASE_DIR, 'static'),
    # )

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
    # STATICFILES_FINDERS = (
    #     'django.contrib.staticfiles.finders.FileSystemFinder',
    #     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # )
    # END STATIC FILE CONFIGURATION

    # MEDIA CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
    MEDIA_ROOT = join(BASE_DIR, "media")

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
    MEDIA_URL = "/media/"
    # END MEDIA CONFIGURATION

    # URL Configuration
    ROOT_URLCONF = "invo.urls"

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
    WSGI_APPLICATION = "invo.wsgi.application"
    # End URL Configuration

    # AUTHENTICATION CONFIGURATION
    # AUTHENTICATION_BACKENDS = (
    #     'django.contrib.auth.backends.ModelBackend',
    # )

    # Password validation
    # https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    # END AUTHENTICATION CONFIGURATION

    # LOGGING CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
    # See http://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
        "handlers": {
            "mail_admins": {
                "level": "ERROR",
                "filters": ["require_debug_false"],
                "class": "django.utils.log.AdminEmailHandler",
            }
        },
        "loggers": {
            "django.request": {
                "handlers": ["mail_admins"],
                "level": "ERROR",
                "propagate": True,
            },
        },
    }
    # END LOGGING CONFIGURATION

    @classmethod
    def post_setup(cls):
        cls.DATABASES["default"]["ATOMIC_REQUESTS"] = True

    # Waffle app
    WAFFLE_FLAG_DEFAULT = values.BooleanValue(False)
    WAFFLE_SWITCH_DEFAULT = values.BooleanValue(False)
    WAFFLE_SAMPLE_DEFAULT = values.BooleanValue(False)

    HAYSTACK_CONNECTIONS = values.SearchURLValue('elasticsearch://127.0.0.1:9200/invo')
    HAYSTACK_FUZZY_MIN_SIM = 0.2
    HAYSTACK_FUZZY_MAX_EXPANSIONS = 50

    # INVO APP SETTINGS

    # instance namespace used to distinguish different invo instances, if needed
    # TODO: maybe tie to sites framework?
    # nullable
    INVO_APP_IRN_NAMESPACE = values.Value("stage")
    # INVO_APP_IRN_NAMESPACE = None
