from challenge.exceptions.api import NotFound


class CatalogException(Exception):
    pass


class CatalogResponseException(CatalogException):
    def __init__(self, response):
        self.response = response
        super().__init__(
            'Failed request. '
            f'Reason: {response.reason}, '
            f'code: {response.status}'
        )


class ProductNotFound(NotFound):
    message = 'Product not found.'
