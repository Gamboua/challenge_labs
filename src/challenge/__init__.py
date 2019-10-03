import django  # isort:skip
django.setup()

from .factory.build_app import build_app  # noqa
from .version import __version__  # noqa

app = build_app()
