import pytest
from simple_settings import settings


@pytest.fixture
def product_id():
    return '6c49be9c-f87f-9791-73fc-ce5b7c5d44db'


@pytest.fixture
def catalog_url(product_id):
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
