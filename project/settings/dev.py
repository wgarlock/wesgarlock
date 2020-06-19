import os

import dj_database_url
import environ

from project.settings import BASE_DIR

env = environ.Env(DEBUG=(bool, False))


def optenv(var):
    return env(var, default=None)


env.read_env(os.path.join(BASE_DIR, '.env'))

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {'default': dj_database_url.config(default=env('DATABASE_URL_DEV', default=''))}

DEV_APPS = [
    "debug_toolbar"
]

DEV_MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    '127.0.0.1',
]