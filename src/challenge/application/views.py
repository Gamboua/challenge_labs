import logging

from aiohttp import web

from challenge.exceptions.api import Unauthorized

from .models import Application
from .serializers import TokenCreateSerializer

logger = logging.getLogger(__name__)


class TokenCreateView(web.View):

    async def post(self):
        data = await self.request.json()
        serializer = TokenCreateSerializer(strict=True).load(data).data

        application = Application.authenticate(
            client_id=serializer['client_id'],
            client_secret=serializer['client_secret']
        )

        if not application:
            raise Unauthorized()

        logger.info(
            f'Create token for application {application.name}'
        )

        application_token = application.create_token()

        return web.json_response(application_token.as_dict())
