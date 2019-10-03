import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import View

from challenge.application.decorators import (
    _get_application,
    _get_token_claims,
    _validate_signature,
    auth_required
)
from challenge.application.models import Application
from challenge.exceptions.api import Unauthorized


class ViewStub(View):
    @auth_required
    async def post(self):
        return web.Response()


class RequestStub:
    def __init__(self, token=None):
        self.method = 'POST'
        self.headers = {'Authorization': f'Bearer {token}'}


@pytest.mark.django_db
class TestAuthRequired:
    async def test_should_return_authorized_application(self, token):
        response = await ViewStub(RequestStub(token))

        assert response.status == 200

    async def test_should_return_unauthorized_on_missing_token(self):
        with pytest.raises(Unauthorized):
            await ViewStub(RequestStub())

    async def test_should_return_unauthorized_on_invalid_token(self):
        token = (
            'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.'
            'eyJpZCI6MSwibmFtZSI6Ikxpc2EgQnVybnMiLCJleHAiOjE1MDc5MjUxMzd9'
        )
        request = RequestStub(token)

        with pytest.raises(Unauthorized):
            response = await ViewStub(request)
            assert 'Invalid token' in response.text

    async def test_should_return_unauthorized_on_expired_token(
        self,
        expired_token,
    ):
        with pytest.raises(Unauthorized):
            await ViewStub(RequestStub(expired_token))

    async def test_should_return_unauthorized_on_invalid_application(
        self,
        token
    ):
        Application.objects.all().delete()

        with pytest.raises(Unauthorized):
            await ViewStub(RequestStub(token))

    async def test_should_raise_unauthorized_on_invalid_payload_info(
        self,
        token
    ):
        payload = _get_token_claims(token)
        payload.pop('id')

        with pytest.raises(Unauthorized):
            _get_application(payload)

    async def test_should_return_unauthorized_on_inactive_application(
        self,
        application,
        token,
    ):
        application.is_active = False
        application.save()

        with pytest.raises(Unauthorized):
            await ViewStub(RequestStub(token))

    async def test_should_raise_unauthorized_on_invalid_secret_key(
        self,
        application,
        token,
    ):
        key = 'xablau'
        with pytest.raises(Unauthorized):
            _validate_signature(application, token, key)
