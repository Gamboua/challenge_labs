import logging

from aiohttp import web
from django.db.utils import DatabaseError

from .models import Customer
from .serializers import CustomerSerializer

logger = logging.getLogger(__name__)


class CustomerView(web.View):
    async def get(self):
        customer_email = self.request.match_info.get('email')

        customer = Customer.objects.filter(email=customer_email).first()
        result = CustomerSerializer().dump(customer).data

        return web.json_response(result, status=200)

    async def post(self):
        customer_email = self.request.match_info.get('email')
        data = await self.request.json()

        serializer = CustomerSerializer(
            strict=True
        ).load(data).data
        serializer['email'] = customer_email

        try:
            customer, created = Customer.objects.filter(
                email=customer_email
            ).get_or_create(
                **serializer
            )

            result = CustomerSerializer().dump(
                customer
            ).data

        except DatabaseError:
            logger.error(
                f'Fail to persist customer {serializer}'
            )

        return web.json_response(result, status=201)
