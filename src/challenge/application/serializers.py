from marshmallow import Schema, fields

from challenge.helpers.serializer.mixins import HandleErrorMixin


class TokenCreateSerializer(HandleErrorMixin, Schema):
    client_id = fields.String(required=True)
    client_secret = fields.String(required=True)
