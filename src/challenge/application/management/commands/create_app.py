from django.core.management.base import BaseCommand

from challenge.application.models import Application

from .templates import NEW_APP_INFO, TEXT_NO, TEXT_YES


class Command(BaseCommand):
    help = 'Creates a new App. Usage: django-admin createapp <app_name>'

    def add_arguments(self, parser):  # pragma: no cover
        parser.add_argument('name', type=str)

    def handle(self, *args, **options):
        application = Application(name=options['name'])
        application.save()

        print(
            NEW_APP_INFO.format(
                app_id=application.id,
                name=application.name,
                client_id=application.client_id,
                client_secret=application.client_secret,
                is_active=(TEXT_YES if application.is_active else TEXT_NO),
                token=application.create_token().token
            )
        )
