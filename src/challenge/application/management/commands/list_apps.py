from django.core.management.base import BaseCommand
from django.core.paginator import Paginator

from challenge.application.models import Application

from .templates import (
    APP_INFO,
    APP_PAGE_INFO,
    APP_QUERY_INFO,
    SEPARATOR,
    TEXT_NO,
    TEXT_YES
)


class Command(BaseCommand):
    help = (
        'List Apps. Usage: django-admin listapps --app=<app_name> '
        '--is-active=[true | false] --limit=<results_per_page> '
        '--page=<page_number>'
    )

    def add_arguments(self, parser):  # pragma: no cover
        parser.add_argument('--app', type=str, required=False)
        parser.add_argument(
            '--is-active',
            dest='is_active',
            type=str,
            choices=['true', 'false', ''],
            required=False
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=30,
            required=False
        )
        parser.add_argument(
            '--page',
            type=int,
            default=1,
            required=False
        )

    def handle(self, *args, **options):
        filters = {}
        if options['app']:
            filters['name'] = options['app']

        if options['is_active']:
            filters['is_active'] = (
                True if options['is_active'] == 'true' else False
            )

        paginator = Paginator(
            Application.objects.filter(**filters).order_by('id'),
            options['limit']
        )

        page_text = APP_PAGE_INFO.format(page=options['page'])

        self.stdout.write(APP_QUERY_INFO.format(
            count=paginator.count,
            num_pages=paginator.num_pages
        ))
        self.stdout.write(page_text)
        self.stdout.write(SEPARATOR)

        self.stdout.write(self.__get_applications_output(
            paginator.page(options['page'])
        ))

        self.stdout.write(page_text)

    @staticmethod
    def __get_applications_output(page):
        output = ''
        for app in page:
            output += APP_INFO.format(
                app_id=app.id,
                name=app.name,
                client_id=app.client_id,
                client_secret=app.client_secret,
                is_active=(TEXT_YES if app.is_active else TEXT_NO),
                token=app.create_token().token
            )
            output += SEPARATOR

        return output
