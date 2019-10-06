from .views import CustomerView

CUSTOMER_ROUTES = [
    ('*', r'/customer/{email}/', CustomerView, 'customer'),
]
