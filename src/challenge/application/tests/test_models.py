import pytest
from model_mommy import mommy

from challenge.application.models import Application, ApplicationToken


@pytest.mark.django_db
class TestApplicationModel:

    @pytest.fixture
    def active_application(self):
        return mommy.make(Application, name='my app', client_id='1234')

    @pytest.fixture
    def inactive_application(self):
        return mommy.make(Application, is_active=False)

    def test_representation(self, active_application):
        assert repr(active_application) == '<Application my app - 1234>'

    def test_should_auto_generate_client_id(self):
        app = Application.objects.create(name='app')

        assert len(app.client_id) == 32

    def test_should_auto_generate_client_secret(self):
        app = Application.objects.create(name='app')

        assert len(app.client_secret) == 64

    def test_should_return_app_when_autenticate(self, active_application):
        app = Application.authenticate(
            client_id=active_application.client_id,
            client_secret=active_application.client_secret
        )

        assert isinstance(app, Application)

    def test_should_return_none_when_autenticate_inactive_application(
        self,
        inactive_application
    ):
        app = Application.authenticate(
            client_id=inactive_application.client_id,
            client_secret=inactive_application.client_secret
        )

        assert app is None

    def test_should_return_none_when_autenticate_non_existent_application(
        self
    ):
        app = Application.authenticate(client_id='', client_secret='')

        assert app is None

    def test_should_return_application_token(self, active_application):
        token = active_application.create_token()

        assert isinstance(token, ApplicationToken)


@pytest.mark.django_db
class TestApplicationToken:

    def test_as_dict_payload(self):
        token = ApplicationToken(token='zé', expires_in=1234)
        expected = {
            'token': 'zé',
            'expires_in': 1234
        }

        assert token.as_dict() == expected
