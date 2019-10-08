from .views import CustomerView, WishListView

CUSTOMER_ROUTES = [
    (
        '*',
        r'/customer/{email}/',
        CustomerView,
        'customer'
    ),
    (
        '*',
        r'/customer/{email}/wishlist/',
        WishListView,
        'customer-wishlist-list-create'
    )
]
