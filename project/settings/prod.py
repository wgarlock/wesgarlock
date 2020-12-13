import logging.config
import os

import dj_database_url
import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://8f938dcf8b2943e29b84180082a32afd@o486641.ingest.sentry.io/5544255",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

root = environ.Path(__file__) - 3

BASE_DIR = root()

env = environ.Env(DEBUG=(bool, False))


def optenv(var):
    return env(var, default=None)


env.read_env(os.path.join(BASE_DIR, '.env'))

ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST ', default=None)
EMAIL_PORT = env('EMAIL_PORT', default=None)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default=None)
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default=None)
EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=None)
EMAIL_USE_SSL = env('EMAIL_USE_SSL', default=None)
EMAIL_TIMEOUT = env('EMAIL_TIMEOUT', default=None)
EMAIL_SSL_KEYFILE = env('EMAIL_SSL_KEYFILE', default=None)
EMAIL_SSL_CERTFILE = env('EMAIL_SSL_CERTFILE', default=None)


SECRET_KEY = env('SECRET_KEY', default=None)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env('REDIS_CACHE_URL', default=None),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
HTML_MINIFY = True

AWS_S3_OBJECT_PARAMETERS = {
    'Access-Control-Allow-Origin': '*'
}

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default="")
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default="")
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', default="")
AWS_REGION = env('AWS_REGION', default="nyc3")
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME ', default="nyc3")
AWS_S3_ENDPOINT_URL = f"https://{AWS_S3_REGION_NAME}.digitaloceanspaces.com"
AWS_S3_SECURE_URLS = True
AWS_PRELOAD_METADATA = env("AWS_PRELOAD_METADATA", default=True)
AWS_QUERYSTRING_AUTH = env("AWS_QUERYSTRING_AUTH", default=True)
AWS_IS_GZIPPED = env("AWS_IS_GZIPPED", default=True)
AWS_S3_SECURE_URLS = env("AWS_S3_SECURE_URLS", default=True)
AWS_DEFAULT_ACL = None
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'project.aws.StaticRootStorage'
DEFAULT_FILE_STORAGE = 'project.aws.MediaRootStorage'
AWS_UPLOAD_EXPIRATION = env("AWS_UPLOAD_EXPIRATION", default=10)
AWS_QUERYSTRING_EXPIRE = AWS_UPLOAD_EXPIRATION
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': str('public, max-age=31536000'),
}
AWS_HEADERS = {
    'Expires': AWS_UPLOAD_EXPIRATION,
    'CacheControl': str('public, max-age=86400'),
}

CLOUDFRONT_ID = env('CLOUDFRONT_ID', default=None)
if env('CLOUDFRONT_ID', default=None):
    CLOUDFRONT_ID = env('CLOUDFRONT_ID', default=None)

    CLOUDFRONT_DOMAIN = f"{CLOUDFRONT_ID}.cloudfront.net"

    if CLOUDFRONT_ID:
        AWS_S3_CUSTOM_DOMAIN = CLOUDFRONT_ID

    WAGTAILFRONTENDCACHE = {
        'cloudfront': {
            'BACKEND': 'wagtail.contrib.frontend_cache.backends.CloudfrontBackend',
            'DISTRIBUTION_ID': f'{CLOUDFRONT_ID}',
        },
    }

RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY', default='')
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY ', default='')

AWS_IS_GZIPPED = True

DATABASES = {'default': dj_database_url.config(default=env('DATABASE_URL_PROD', default=''))}

# Clear prev config
LOGGING_CONFIG = None

# Get loglevel from env
LOGLEVEL = os.getenv('DJANGO_LOGLEVEL', 'info').upper()

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {
            'level': LOGLEVEL,
            'handlers': ['console'],
        },
    },
})
