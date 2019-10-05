import pytest

from challenge.customer.serializers import CustomerSerializer
from challenge.exceptions.api import ValidationError


class TestCustomerSerializer:
    @pytest.fixture
    def payload(self):
        return {
            'name': 'Fulano',
            'email': 'fulano@gmail.com'
        }

    def test_serializer_should_raise_when_invalid_email(self, payload):
        payload['email'] = 'fufufu'

        with pytest.raises(ValidationError):
            CustomerSerializer().load(payload).data
