from marshmallow import Schema, fields

from challenge.helpers.serializer.mixins import HandleErrorMixin


class CustomerSerializer(HandleErrorMixin, Schema):
    id = fields.Int()
    name = fields.String()
    email = fields.Email()


class WishListSerializer(HandleErrorMixin, Schema):
    customer = fields.Email(required=True)
    product_id = fields.UUID(required=True)
