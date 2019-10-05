from .views import CustomerView


CUSTOMER_ROUTES = [
    ('*', r'/customer/', CustomerView, 'customer'),
]
