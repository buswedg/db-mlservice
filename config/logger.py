import os
import logging
from .settings.common import DEBUG, BASE_DIR

log = logging.getLogger(__name__)

if DEBUG:
    min_level = "DEBUG"
else:
    min_level = "INFO"

min_django_level = "INFO"

LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_FILE = "django.log"
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)
open(LOG_PATH, 'a').close()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'timestampthread': {
            'format': "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [%(name)-20.20s]  %(message)s",
        },
    },
    'handlers': {
        'logfile': {
            'level': min_level,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH,
            'maxBytes': 50 * 10 ** 6,
            'backupCount': 3,
            'formatter': 'timestampthread'
        },
        'console': {
            'level': min_level,
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['logfile', 'console'],
            'level': min_django_level,
            'propagate': False,
        },
        'custom': {
            'handlers': ['logfile', 'console'],
            'level': min_level,
        },
    },
}
