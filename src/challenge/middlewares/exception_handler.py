import logging
from json.decoder import JSONDecodeError

from aiohttp import web
from aiohttp.web import middleware
from aiohttp.web_exceptions import HTTPError
from django.http.response import Http404

from challenge.exceptions.api import APIException, ErrorDetail

logger = logging.getLogger(__name__)


@middleware
async def exception_handler_middleware(request, handler):
    try:
        return (await handler(request))
    except APIException as exc:
        payload = exc.get_full_details()
        status_code = exc.status_code
    except HTTPError as exc:
        status_code = exc.status_code
        payload = ErrorDetail(
            code='generic_error',
            message=exc.reason,
            details=None
        )._asdict()
    except Http404:
        status_code = 404
        payload = ErrorDetail(
            code='not_found',
            message='Entity not found.',
            details=None
        )._asdict()
    except JSONDecodeError:
        status_code = 400
        payload = ErrorDetail(
            code='request_error',
            message='Expected a valid JSON payload.',
            details=None
        )._asdict()
    except Exception as exc:
        api_exception = APIException()
        payload = api_exception.get_full_details()
        status_code = api_exception.status_code
        logger.critical(
            f'Exception: {exc}; '
            f'Name: {exc.__class__.__name__}'
        )

    return web.json_response(
        payload,
        status=status_code
    )
