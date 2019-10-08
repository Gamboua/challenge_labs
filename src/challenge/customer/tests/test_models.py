import pytest
from model_mommy import mommy


@pytest.fixture
def customer():
    return mommy.make(
        'customer.Customer',
        id=2,
        name='Fulano',
        email='fulano@gmail.com'
    )


@pytest.fixture
def wishlist(customer, product_id):
    return mommy.make(
        'customer.Wishlist',
        id=1,
        customer=customer,
        product_id=product_id
    )


@pytest.mark.django_db
class TestCustomer:

    def test_customer_should_have_name(self, customer):
        assert 'Fulano' == customer.name

    def test_customer_should_have_email(self, customer):
        assert 'fulano@gmail.com' == customer.email


@pytest.mark.django_db
class TestWishList:
    def test_wishlist_should_have_product_id(
        self,
        wishlist,
        product_id
    ):
        assert product_id == wishlist.product_id

    def test_wishlist_should_have_customer(self, wishlist, customer):
        assert customer == wishlist.customer
