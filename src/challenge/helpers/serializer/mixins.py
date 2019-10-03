from challenge.exceptions.api import ValidationError


class HandleErrorMixin:
    """
    Marshmallow implementation
    """
    def handle_error(self, exc, data):
        raise ValidationError(details=exc.messages)
