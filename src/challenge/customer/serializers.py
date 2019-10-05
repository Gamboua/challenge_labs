from marshmallow import Schema, fields, post_load
from challenge.helpers.serializer.mixins import HandleErrorMixin
from .models import Customer


class CustomerSerializer(HandleErrorMixin, Schema):
    id = fields.Int()

    name = fields.String()
    email = fields.Email()

    @post_load
    def make_customer(self, data, **kwargs):
        return Customer(**data)
