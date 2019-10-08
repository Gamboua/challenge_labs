import logging

from aiohttp import web
from django.db.utils import DatabaseError

from challenge.application.decorators import auth_required
from challenge.extensions.catalog.http_client import get_product_by_id

from .exceptions import CustomerNotFound
from .helpers import build_wishlist_response
from .models import Customer, WishList
from .serializers import CustomerSerializer, WishListSerializer

logger = logging.getLogger(__name__)


class CustomerView(web.View):

    @auth_required
    async def get(self):
        customer_email = self.request.match_info.get('email')

        try:
            customer = Customer.objects.get(email=customer_email)
            result = CustomerSerializer().dump(customer).data

            return web.json_response(result, status=200)
        except Customer.DoesNotExist:
            raise CustomerNotFound()

    @auth_required
    async def post(self):
        customer_email = self.request.match_info.get('email')
        data = await self.request.json()

        serializer = CustomerSerializer(
            strict=True
        ).load(data).data
        serializer['email'] = customer_email

        try:
            customer, _ = Customer.objects.filter(
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

    @auth_required
    async def put(self):
        customer_email = self.request.match_info.get('email')
        data = await self.request.json()

        serializer = CustomerSerializer(strict=True).load(data).data
        serializer['email'] = customer_email

        update = Customer.objects.filter(
            email=customer_email
        ).update(**serializer)

        if not update:
            raise CustomerNotFound(
                message='Fail to update customer.'
            )

        return web.json_response(status=204)

    @auth_required
    async def delete(self):
        Customer.objects.filter(
            email=self.request.match_info.get('email')
        ).delete()

        return web.json_response(status=204)


class WishListView(web.View):

    @auth_required
    async def get(self):
        customer_email = self.request.match_info.get('email')

        customer = Customer.objects.get(
            email=customer_email
        )

        wishlist = WishList.objects.filter(
            customer=customer
        )

        result = await build_wishlist_response(
            wishlist=wishlist
        )

        return web.json_response(result, status=200)

    @auth_required
    async def post(self):
        customer_email = self.request.match_info.get('email')
        data = await self.request.json()

        data['customer'] = customer_email

        serializer = WishListSerializer(
            strict=True
        ).load(data).data

        customer = Customer.objects.get(
            email=serializer['customer']
        )

        if not customer:
            raise CustomerNotFound

        product = await get_product_by_id(
            product_id=serializer['product_id']
        )

        wishlist, _ = WishList.objects.filter(
            customer=customer,
            product_id=product['id']
        ).get_or_create(
            {
                'customer': customer,
                'product_id': serializer['product_id']
            }
        )

        result = WishListSerializer().dump(
            {
                'customer': wishlist.customer.email,
                'product_id': wishlist.product_id
            }
        ).data

        return web.json_response(result, status=201)
