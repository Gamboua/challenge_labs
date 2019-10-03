from aiohttp.web import middleware

from challenge.version import __version__


@middleware
async def version_middleware(request, handler):
    response = await handler(request)
    response.headers['X-API-Version'] = __version__
    return response
