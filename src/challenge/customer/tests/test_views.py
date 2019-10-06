import pytest

from challenge.customer.models import Customer


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
