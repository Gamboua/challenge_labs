import logging
from functools import wraps

from jose import ExpiredSignatureError, JWTError, jwt
from jose.jwt import get_unverified_claims

from challenge.application.helpers import create_jwt_key
from challenge.application.models import Application
from challenge.exceptions.api import Unauthorized

logger = logging.getLogger(__name__)


def auth_required(method):

    @wraps(method)
    def wrapper(self, *args, **kwargs):

        token = _get_header_token(self)
        payload = _get_token_claims(token)
        application = _get_application(payload)

        key = create_jwt_key(application)
        _validate_signature(application, token, key)

        return method(self, *args, **kwargs)

    return wrapper


def _get_header_token(view):
    authorization_header = view.request.headers.get('Authorization', '')
    if 'Bearer' not in authorization_header:
        raise Unauthorized(message='Invalid authorization header.')

    return authorization_header.replace('Bearer', '').strip()


def _get_token_claims(token):
    try:
        return get_unverified_claims(token)
    except JWTError:
        raise Unauthorized(message='Invalid token.')


def _get_application(payload):
    try:
        return Application.objects.get(id=payload['id'], is_active=True)
    except KeyError:
        logger.info('Invalid token.')
        raise Unauthorized(message='Invalid token.')
    except Application.DoesNotExist:
        logger.info(f'Application {payload["id"]} not found.')
        raise Unauthorized()


def _validate_signature(application, token, key):
    try:
        jwt.decode(token, key)
    except ExpiredSignatureError:
        raise Unauthorized(message='Expired token.')
    except JWTError:
        logger.info(f'Failed to authenticate {application}.')
        raise Unauthorized()
