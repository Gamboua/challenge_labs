import pytest


@pytest.mark.django_db
class TestTokenCreateView:

    @pytest.fixture
    def url(self, app):
        return app.router['token-create'].url_for()

    @pytest.fixture
    def invalid_paylod(self):
        return {}

    @pytest.fixture
    def valid_payload(self):
        return {'client_id': 'dou', 'client_secret': 'gras'}

    async def test_should_raise_validation_error(
        self,
        client,
        url,
        invalid_paylod
    ):
        response = await client.post(path=url, json=invalid_paylod)
        data = await response.json()

        assert response.status == 400
        assert data['message'] == 'Invalid input.'

    async def test_should_return_unauthorized_when_application_does_not_exist(
        self,
        client,
        url,
        valid_payload
    ):
        response = await client.post(path=url, json=valid_payload)
        data = await response.json()

        assert response.status == 401
        assert data['message'] == 'Unauthorized.'

    async def test_should_return_applicaton_token(
        self,
        client,
        url,
        application
    ):
        payload = {
            'client_id': application.client_id,
            'client_secret': application.client_secret
        }

        response = await client.post(path=url, json=payload)
        data = await response.json()

        assert response.status == 200
        assert 'token' in data
        assert 'expires_in' in data
