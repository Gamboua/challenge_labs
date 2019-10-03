from .views import TokenCreateView

APPLICATION_ROUTES = [
    (
        '*',
        r'/application/token/',
        TokenCreateView,
        'token-create'
    ),
]
