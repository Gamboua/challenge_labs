from collections import namedtuple
from contextlib import suppress

from django.db import models
from jose import jwt
from simple_settings import settings

from .helpers import (
    create_jwt_claims,
    create_jwt_key,
    generate_application_client_id,
    generate_application_client_secret
)


class ApplicationToken(
    namedtuple('ApplicationToken', ['token', 'expires_in'])
):
    def as_dict(self):
        return {
            'token': self.token,
            'expires_in': int(self.expires_in)
        }


class Application(models.Model):
    name = models.CharField(max_length=56, db_index=True)
    client_id = models.CharField(
        max_length=32,
        default=generate_application_client_id
    )
    client_secret = models.CharField(
        max_length=64,
        default=generate_application_client_secret
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'application'
        unique_together = ('client_id', 'client_secret')

    def __repr__(self):
        return f'<Application {self.name} - {self.client_id}>'

    @staticmethod
    def authenticate(client_id, client_secret):
        with suppress(Application.DoesNotExist):
            return Application.objects.get(
                client_id=client_id,
                client_secret=client_secret,
                is_active=True
            )

    def create_token(self):
        jwt_payload = create_jwt_claims(self)
        jwt_key = create_jwt_key(self)
        token = jwt.encode(
            claims=jwt_payload,
            key=jwt_key,
            algorithm='HS256'
        )

        return ApplicationToken(
            token=token,
            expires_in=settings.APPLICATION_TOKEN_EXPIRE_TIME
        )
