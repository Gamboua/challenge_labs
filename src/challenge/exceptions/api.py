from collections import namedtuple

ErrorDetail = namedtuple('ErrorDetail', ['code', 'message', 'details'])


class APIException(Exception):
    status_code = 500
    code = 'server_error'
    message = 'A server error occured.'
    details = None

    def __init__(self, code=None, message=None, details=None):
        if code:
            self.code = code

        if message:
            self.message = message

        if details:
            self.details = details

    def get_full_details(self):
        return ErrorDetail(
            code=self.code,
            message=self.message,
            details=self.details
        )._asdict()


class ValidationError(APIException):
    status_code = 400
    code = 'invalid'
    message = 'Invalid input.'


class NotFound(APIException):
    status_code = 404
    code = 'not_found'
    message = 'Not found.'


class DatabaseAPIException(APIException):
    code = 'database_error'


class Unauthorized(APIException):
    status_code = 401
    code = 'unauthorized'
    message = 'Unauthorized.'
