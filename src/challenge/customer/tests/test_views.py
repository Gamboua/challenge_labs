import pytest

from challenge.customer.models import Customer


@pytest.mark.django_db
class TestCustomerView:

    @pytest.fixture
    def valid_payload(self):
        return {
            'name': 'Fulano',
            'email': 'fulano@gmail.com'
        }

    async def test_should_successfully_get_customer(
        self,
        client,
        customer,
        customer_url
    ):
        response = await client.get(path=customer_url)

        assert response.status == 200
        response = await response.json()
        assert response['email'] == customer.email

    async def test_should_create_customer(
        self,
        client,
        customer_url,
        valid_payload
    ):
        response = await client.post(
            path=customer_url,
            json=valid_payload
        )

        assert response.status == 201

        data = await response.json()

        assert data['name'] == valid_payload['name']
        assert data['email'] == valid_payload['email']

    async def test_should_return_aways_the_same_customer_when_using_same_email(
        self,
        client,
        customer_url,
        valid_payload
    ):
        assert len(Customer.objects.all()) == 0

        for _ in range(2):
            await client.post(
                path=customer_url,
                json=valid_payload
            )

        assert len(Customer.objects.all()) == 1
