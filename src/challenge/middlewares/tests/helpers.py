from aiohttp import web


async def handler_success_return(request):
    return web.json_response({'message': 'success'})
