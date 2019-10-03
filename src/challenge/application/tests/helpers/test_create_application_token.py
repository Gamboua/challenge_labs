from datetime import datetime
from unittest.mock import patch

import pytest

from challenge.application.helpers import create_jwt_claims, create_jwt_key
from challenge.application.models import Application


class TestCreateApplicationToken:

    @pytest.fixture
    def application(self):
        return Application(
            id=1,
            name='app_name',
            client_id='client_id',
            client_secret='client_secret'
        )

    @pytest.fixture
    def patch_jwt(self):
        with patch('jose.jwt.encode') as patch_jwt:
            yield patch_jwt

    @pytest.fixture
    def patch_claims(self):
        with patch(
            'challenge.application.models.create_jwt_claims',
            return_value={}
        ) as patch_claims:
            yield patch_claims

    def test_jwt_claims_payload(self, application):
        payload = create_jwt_claims(application)

        assert payload['id'] == application.id
        assert payload['name'] == application.name
        assert isinstance(payload['exp'], datetime)

    def test_should_call_create_jwt_claims(self, application, patch_claims):
        application.create_token()

        patch_claims.assert_called_with(application)

    def test_should_call_jose_to_generate_token(
        self,
        application,
        patch_jwt,
        patch_claims
    ):
        application.create_token()

        patch_jwt.assert_called_with(
            algorithm='HS256',
            claims={},
            key=create_jwt_key(application)
        )
