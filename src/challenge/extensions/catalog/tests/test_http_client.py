import pytest
from aiohttp import ClientError
from aioresponses import aioresponses

from challenge.extensions.catalog.exceptions import (
    CatalogException,
    CatalogResponseException
)
from challenge.extensions.catalog.http_client import get_product_by_id


class TestGetProductById:

    async def test_should_get_product(
        self,
        product_id,
        catalog_response,
        catalog_url
    ):

        with aioresponses() as m:
            m.get(
                catalog_url,
                payload=catalog_response
            )

            response_payload = await get_product_by_id(
                product_id=product_id
            )

            assert response_payload == catalog_response

    async def test_should_raises_response_exception(
        self,
        product_id,
        catalog_url
    ):

        with aioresponses() as m:
            m.get(
                catalog_url,
                status=400
            )

            with pytest.raises(CatalogResponseException):
                await get_product_by_id(product_id)

    async def test_should_raises_client_error_exception(
        self,
        product_id,
        catalog_url
    ):

        with aioresponses() as m:
            m.get(
                catalog_url,
                exception=ClientError()
            )

            with pytest.raises(CatalogException):
                await get_product_by_id(
                    product_id='de83aecc-d490-4d96-8b0c-6c857a4736de'
                )
