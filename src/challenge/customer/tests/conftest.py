import pytest
from model_mommy import mommy


@pytest.fixture
def customer_email():
    return 'fulano@gmail.com'


@pytest.fixture
def customer(customer_email):
    return mommy.make(
        'customer.Customer',
        email=customer_email
    )


@pytest.fixture
def customer_url(app, customer_email):
    return app.router['customer'].url_for(email=customer_email)
