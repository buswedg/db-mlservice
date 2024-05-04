from .common import *

INTERNAL_IPS = ['127.0.0.1']

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------

default_loaders = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

for options in TEMPLATES:
    options['OPTIONS']['loaders'] = default_loaders
