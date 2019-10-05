from challenge.application.routes import APPLICATION_ROUTES
from challenge.customer.routes import CUSTOMER_ROUTES

ROUTES = []

ROUTES += APPLICATION_ROUTES
ROUTES += CUSTOMER_ROUTES


def setup_routes(app):
    for http_method, endpoint, handler, name in ROUTES:
        app.router.add_route(
            method=http_method,
            path=endpoint,
            handler=handler,
            name=name
        )
