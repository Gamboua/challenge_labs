import os
import sys
from decimal import Decimal
from distutils.util import strtobool

import dj_database_url

from . import constants

DEBUG = bool(
    strtobool(os.getenv('DEBUG', 'False'))
)

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))

# 'postgresql://user:pass@localhost/mydatabase'
DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///challenge.db')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'add_hostname': {
            '()': 'challenge.helpers.logs.filters.AddHostName'
        },
        'not_healthcheck': {
            '()': 'challenge.helpers.logs.filters.NotIncludeHealthcheck'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(hostname)s %(levelname)s %(asctime)s %(name)s %(module)s %(process)d %(thread)d %(message)s'  # noqa
        },
        'simple': {
            'format': '%(hostname)s %(levelname)s %(name)s %(message)s'
        },
        'syslog': {
            'format': '%(asctime)s %(hostname)s %(name)s: %(filename)s:%(lineno)d %(process)d %(thread)d %(message)s\n',  # noqa
            'datefmt': '%b %d %H:%M:%S',
        },
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'DEBUG',
            'stream': sys.stdout,
            'filters': ['add_hostname', 'not_healthcheck']
        }
    },
    'loggers': {
        '': {
            'handlers': ['stdout'],
            'level': 'ERROR',
            'propagate': True,
        },
        'aiohttp': {
            'handlers': ['stdout'],
            'level': 'ERROR',
            'propagate': False,
        },
        'challenge': {
            'handlers': ['stdout'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}

AIO_CACHES = {
    'default': {
        'cache': 'aiocache.SimpleMemoryCache',
        'serializer': {
            'class': 'aiocache.serializers.JsonSerializer'
        }
    },
}

APPLICATION_TOKEN_EXPIRE_TIME = 7 * constants.DAYS

# DJANGO
ALLOWED_HOSTS = ['*']
USE_TZ = True
TIME_ZONE = 'UTC'
STATIC_URL = '/static/'
INSTALLED_APPS = [
    'django.contrib.contenttypes',

    # 'django_celery_beat',

    'challenge.application',
    'challenge.customer'
    # 'dmitri.extensions.correios',
    # 'dmitri.freight',
    # 'dmitri.cities',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SECRET_KEY = 'a4337bc45a8fc544c03f52dc550cd6e1e87021bc896588bd79e901e2'
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URI)
}

DATABASES_POSTGRES_STATEMENT_TIMEOUT = int(
    os.getenv('DATABASES_POSTGRES_STATEMENT_TIMEOUT', '1')
) * 1000

DATABASES_POSTGRES_STATEMENT_TIMEOUT_MIGRATION = int(
    os.getenv('DATABASES_POSTGRES_STATEMENT_TIMEOUT_MIGRATION', '300')
) * 1000
