from aiohttp.test_utils import make_mocked_request

from challenge.middlewares.version import version_middleware

from .helpers import handler_success_return


class TestVersionMiddleware:

    async def test_should_include_header_x_api_version_on_response(
        self,
        client
    ):
        response = await version_middleware(
            request=make_mocked_request('GET', '/xablau'),
            handler=handler_success_return
        )

        assert 'X-Api-Version' in response.headers
