import asyncio
import datetime

import pytest
from aiocache import caches
from django.utils import timezone
from jose import jwt
from model_mommy import mommy
from simple_settings import settings

from challenge import app as _app
from challenge.application.helpers import create_jwt_key


@pytest.fixture(scope='session')
def loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def app(loop):
    return _app


@pytest.fixture(autouse=True)
def client(aiohttp_client, app, loop):
    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture()
def client_authenticated(aiohttp_client, app, loop, token):
    return loop.run_until_complete(
        aiohttp_client(
            app,
            headers={'Authorization': f'Bearer {token}'}
        )
    )


@pytest.fixture(autouse=True)
def clear_cache(request, loop):
    marker = request.keywords.get('clear_cache', None)
    if marker:
        for key in settings.AIO_CACHES:
            cache = caches.get(key)
            loop.run_until_complete(cache.clear())


@pytest.fixture
def application():
    return mommy.make('application.Application')


@pytest.fixture
def token(application):
    return application.create_token().token


@pytest.fixture
def expired_token(application):
    jwt_key = create_jwt_key(application)
    return jwt.encode(
        claims={
            'id': application.id,
            'name': application.name,
            'exp': timezone.now() - datetime.timedelta(days=1)
        },
        key=jwt_key,
        algorithm='HS256'
    )


@pytest.fixture
def product_id():
    return '6c49be9c-f87f-9791-73fc-ce5b7c5d44dd'


@pytest.fixture
def catalog_url(product_id):
    settings.CATALOG_CONFIG['url'] = 'http://catalog.com'

    catalog_url = settings.CATALOG_CONFIG['url']
    return f'{catalog_url}/api/product/{product_id}'


@pytest.fixture
def catalog_response(product_id):
    return {
        'price': 55.9,
        'image': 'http://challenge-api.luizalabs.com/b.jpg',
        'brand': 'tramontina',
        'id': product_id,
        'title': 'Jogo de Inox para Torta Copacabana 7 Peças'
    }
