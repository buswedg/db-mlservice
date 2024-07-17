from .common import *

# APP DEFINITION
# ------------------------------------------------------------------------------

REDIS_CACHE_ENABLED = os.getenv('DJANGO_REDIS_CACHE_ENABLED', True) == 'True'
if REDIS_CACHE_ENABLED:
    MIDDLEWARE = [
                     'django.middleware.cache.UpdateCacheMiddleware',
                 ] + MIDDLEWARE

    MIDDLEWARE += [
        'django.middleware.cache.FetchFromCacheMiddleware',
    ]

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': 'redis://redis:6379',
        },
    }

    CACHE_MIDDLEWARE_ALIAS = "default"
    CACHE_MIDDLEWARE_KEY_PREFIX = ""
    CACHE_MIDDLEWARE_SECONDS = 600

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------

cached_loaders = (
    'django.template.loaders.cached.Loader',
    [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ],
)

for options in TEMPLATES:
    options['OPTIONS']['loaders'] = [
        cached_loaders,
    ]

# DJANGO REST FRAMEWORK
# ------------------------------------------------------------------------------
# http://www.django-rest-framework.org/

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)
