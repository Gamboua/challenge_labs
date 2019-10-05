import logging
import logging.config

from aiocache import caches
from aiohttp import web
from django.db import connection
from django.db.backends.signals import connection_created
from django.db.models.signals import post_migrate, pre_migrate
from django.dispatch import receiver
from simple_settings import settings

from challenge.middlewares.exception_handler import (
    exception_handler_middleware
)
from challenge.middlewares.version import version_middleware
from challenge.routes import setup_routes

logger = logging.getLogger(__name__)


def build_app():
    app = web.Application(
        middlewares=[
            version_middleware,
            exception_handler_middleware
        ]
    )

    caches.set_config(settings.AIO_CACHES)

    setup_routes(app)

    app.make_handler(
        logger=logging.config.dictConfig(settings.LOGGING),
        debug=settings.DEBUG
    )

    return app


def set_statement_timeout(connection, timeout):
    if connection.vendor != 'postgresql':
        return

    with connection.cursor() as cursor:
        cursor.execute(f'SET statement_timeout TO {timeout};')

        logger.info(f'Set statement_timeout for database {timeout}')


@receiver(connection_created)
def setup_postgres(connection, **kwargs):
    set_statement_timeout(
        connection=connection,
        timeout=settings.DATABASES_POSTGRES_STATEMENT_TIMEOUT
    )


@receiver(pre_migrate)
def pre_migrate_timeout(*args, **kwargs):
    set_statement_timeout(
        connection=connection,
        timeout=settings.DATABASES_POSTGRES_STATEMENT_TIMEOUT_MIGRATION
    )


@receiver(post_migrate)
def post_migrate_timeout(*args, **kwargs):
    set_statement_timeout(
        connection=connection,
        timeout=settings.DATABASES_POSTGRES_STATEMENT_TIMEOUT
    )
