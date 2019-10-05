from marshmallow import Schema, fields

from challenge.helpers.serializer.mixins import HandleErrorMixin


class CustomerSerializer(HandleErrorMixin, Schema):
    id = fields.Int()
    name = fields.String()
    email = fields.Email()
