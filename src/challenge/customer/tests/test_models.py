import pytest

from django.core.exceptions import ValidationError
from model_mommy import mommy


@pytest.mark.django_db
class TestCustomer:

    @pytest.fixture
    def model(self):
        return mommy.make(
            'customer.Customer',
            id=2,
            name='Fulano',
            email='fulano@gmail.com'
        )

    def test_customer_should_have_id(self, model):
        assert 2 == model.id

    def test_customer_should_have_name(self, model):
        assert 'Fulano' == model.name

    def test_customer_should_have_email(self, model):
        assert 'fulano@gmail.com' == model.email
