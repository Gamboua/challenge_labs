from challenge.exceptions.api import NotFound


class CustomerNotFound(NotFound):
    message = 'Customer not found.'
