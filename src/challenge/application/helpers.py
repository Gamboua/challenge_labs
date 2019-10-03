import datetime
import secrets

from django.utils import timezone
from simple_settings import settings


def generate_application_client_id():
    return secrets.token_hex(nbytes=16)


def generate_application_client_secret():
    return secrets.token_hex(nbytes=32)


def create_jwt_claims(application):
    return {
        'id': application.id,
        'name': application.name,
        'exp': timezone.now() + datetime.timedelta(
            seconds=settings.APPLICATION_TOKEN_EXPIRE_TIME
        )
    }


def create_jwt_key(application):
    return f'{application.client_secret}{settings.SECRET_KEY}'
