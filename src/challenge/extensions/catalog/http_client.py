from http import HTTPStatus

import aiohttp
from aiohttp import ClientError, ClientResponseError
from simple_settings import settings

from .exceptions import (
    CatalogException,
    CatalogResponseException,
    ProductNotFound
)


async def get_product_by_id(product_id):

    catalog_url = settings.CATALOG_CONFIG['url']

    catalog_url = f'{catalog_url}/api/product/{product_id}'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=catalog_url
            ) as response:
                status_code = response.status
                response_data = await response.json()

        response.raise_for_status()
    except ClientResponseError as exc:
        if status_code == HTTPStatus.NOT_FOUND:
            raise ProductNotFound()

        raise CatalogResponseException(response) from exc

    except ClientError as exc:
        raise CatalogException() from exc

    return response_data
