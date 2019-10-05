import pytest

from challenge.exceptions.api import ValidationError
from challenge.customer.serializers import CustomerSerializer
from challenge.customer.models import Customer


class TestCustomerSerializer:
    @pytest.fixture
    def payload(self):
        return {
            'name': 'Fulano',
            'email': 'fulano@gmail.com'
        }

    def test_serializer_should_load_customer_object(self, payload):

        data = CustomerSerializer().load(payload).data

        assert isinstance(data, Customer)

    def test_serializer_should_raise_when_invalid_email(self, payload):
        payload['email'] = 'fufufu'

        with pytest.raises(ValidationError):
            CustomerSerializer().load(payload).data
