from unittest import mock

import asynctest
import pytest

from challenge.customer.models import Customer, WishList


@pytest.mark.django_db
class TestCustomerView:

    async def test_should_return_error_if_client_is_not_authenticated(
        self,
        customer_url,
        client
    ):
        response = await client.get(customer_url)
        data = await response.json()

        assert response.status == 401
        assert data['code'] == 'unauthorized'

    async def test_should_successfully_get_customer(
        self,
        client_authenticated,
        customer,
        customer_url
    ):
        response = await client_authenticated.get(path=customer_url)

        assert response.status == 200

        response = await response.json()

        assert response['email'] == customer.email

    async def test_should_return_404_on_customer_not_found(
        self,
        client_authenticated,
        customer_url,
    ):
        response = await client_authenticated.get(
            path=customer_url
        )

        assert response.status == 404

    async def test_should_create_customer(
        self,
        client_authenticated,
        customer_url,
        valid_payload
    ):
        response = await client_authenticated.post(
            path=customer_url,
            json=valid_payload
        )

        assert response.status == 201

        data = await response.json()

        assert data['name'] == valid_payload['name']
        assert data['email'] == valid_payload['email']

    async def test_should_return_aways_the_same_customer_when_using_same_email(
        self,
        client_authenticated,
        customer_url,
        valid_payload
    ):
        assert len(Customer.objects.all()) == 0

        for _ in range(2):
            await client_authenticated.post(
                path=customer_url,
                json=valid_payload
            )

        assert len(Customer.objects.all()) == 1

    async def test_should_successfully_update_customer(
        self,
        client_authenticated,
        valid_payload,
        customer,
        customer_url
    ):
        valid_payload['nome'] = 'Ciclano ferreira'

        response = await client_authenticated.put(
            path=customer_url,
            json=valid_payload
        )

        assert response.status == 204

        customer = Customer.objects.get(
            email=valid_payload['email']
        )

        assert customer.name == valid_payload['name']

    async def test_should_successfully_delete_customer(
        self,
        client_authenticated,
        customer,
        customer_url,
        customer_email
    ):
        response = await client_authenticated.delete(path=customer_url)

        assert response.status == 204
        assert Customer.objects.filter(email=customer_email).count() == 0


@pytest.mark.django_db
class TestWishListView:

    async def test_should_return_error_if_client_is_not_authenticated(
        self,
        customer_url,
        client
    ):
        response = await client.get(customer_url)
        data = await response.json()

        assert response.status == 401
        assert data['code'] == 'unauthorized'

    async def test_should_successfully_get_wishlist(
        self,
        client_authenticated,
        customer,
        wishlist,
        customer_wishlist_url,
        catalog_response
    ):

        with mock.patch(
            'challenge.customer.helpers.get_product_by_id',
            new_callable=asynctest.CoroutineMock,
            return_value=catalog_response
        ):
            response = await client_authenticated.get(
                path=customer_wishlist_url
            )

            assert response.status == 200

            response = await response.json()

        assert response[0]['product'] == catalog_response
        assert response[0]['customer'] == customer.email

    async def test_should_successfully_create_wishlist(
        self,
        client_authenticated,
        customer,
        product_id,
        customer_wishlist_url,
        catalog_response,
        customer_email
    ):

        with mock.patch(
            'challenge.customer.views.get_product_by_id',
            new_callable=asynctest.CoroutineMock,
            return_value=catalog_response
        ):
            response = await client_authenticated.post(
                path=customer_wishlist_url,
                json={'product_id': product_id}
            )

            assert response.status == 201

            response = await response.json()

        assert response['customer'] == customer_email
        assert response['product_id'] == product_id

    async def test_should_not_create_wishlist_with_same_customer_and_product_id_twice( # noqa
        self,
        client_authenticated,
        customer,
        product_id,
        customer_wishlist_url,
        catalog_response
    ):
        with mock.patch(
            'challenge.customer.views.get_product_by_id',
            new_callable=asynctest.CoroutineMock,
            return_value=catalog_response
        ):
            assert len(WishList.objects.all()) == 0

            for _ in range(2):
                await client_authenticated.post(
                    path=customer_wishlist_url,
                    json={'product_id': product_id}
                )

            assert len(WishList.objects.all()) == 1
