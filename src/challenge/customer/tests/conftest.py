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
def wishlist(customer, product_id):
    return mommy.make(
        'customer.Wishlist',
        customer=customer,
        product_id=product_id
    )


@pytest.fixture
def customer_url(app, customer_email):
    return app.router['customer'].url_for(email=customer_email)


@pytest.fixture
def valid_payload(customer_email):
    return {
        'name': 'Fulano',
        'email': customer_email
    }


@pytest.fixture
def customer_wishlist_url(app, customer_email):
    return app.router['customer-wishlist-list-create'].url_for(
        email=customer_email
    )
