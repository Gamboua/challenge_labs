from unittest.mock import patch

import pytest
from model_mommy import mommy

from challenge.application.management.commands.list_apps import Command
from challenge.application.models import ApplicationToken


@pytest.mark.django_db
class TestListAppsCommand:

    @pytest.fixture
    def applications(self):
        return [
            mommy.make('application.Application'),
            mommy.make('application.Application', is_active=False)
        ]

    def test_handle_default(self, capsys, applications):
        cmd = Command()
        cmd.handle(app='', page=1, limit=30, is_active='')

        out, err = capsys.readouterr()

        assert 'Total Pages: 1' in out
        assert ' YES' in out
        assert ' NO' in out

        for app in applications:
            assert app.name in out
            assert app.client_id in out
            assert app.client_secret in out

    def test_handle_limit_first_page(self, capsys, applications):
        cmd = Command()
        cmd.handle(app='', page=1, limit=1, is_active='')

        out, err = capsys.readouterr()

        assert 'Total Pages: 2' in out
        assert ' YES' in out
        assert ' NO' not in out

        assert applications[0].name in out
        assert applications[0].client_id in out
        assert applications[0].client_secret in out

        assert applications[1].name not in out
        assert applications[1].client_id not in out
        assert applications[1].client_secret not in out

    def test_handle_limit_second_page(self, capsys, applications):
        cmd = Command()
        cmd.handle(app='', page=2, limit=1, is_active='')

        out, err = capsys.readouterr()

        assert 'Total Pages: 2' in out
        assert ' YES' not in out
        assert ' NO' in out

        assert applications[1].name in out
        assert applications[1].client_id in out
        assert applications[1].client_secret in out

        assert applications[0].name not in out
        assert applications[0].client_id not in out
        assert applications[0].client_secret not in out

    def test_handle_filter_name(self, capsys, applications):
        cmd = Command()
        cmd.handle(
            app=applications[0].name,
            page=1,
            limit=30,
            is_active=''
        )

        out, err = capsys.readouterr()

        assert 'Total Pages: 1' in out
        assert ' YES' in out
        assert ' NO' not in out

        assert applications[0].name in out
        assert applications[0].client_id in out
        assert applications[0].client_secret in out

        assert applications[1].name not in out
        assert applications[1].client_id not in out
        assert applications[1].client_secret not in out

    def test_handle_filter_is_active_true(self, capsys, applications):
        cmd = Command()
        cmd.handle(app='', page=1, limit=30, is_active='true')

        out, err = capsys.readouterr()

        assert 'Total Pages: 1' in out
        assert ' YES' in out
        assert ' NO' not in out

    def test_handle_filter_is_active_false(self, capsys, applications):
        cmd = Command()
        cmd.handle(app='', page=1, limit=30, is_active='false')

        out, err = capsys.readouterr()

        assert 'Total Pages: 1' in out
        assert ' NO' in out
        assert ' YES' not in out

    def test_should_print_a_valid_token(self, capsys, applications):
        with patch(
            'challenge.application.models.Application.create_token'
        ) as mock_create_token:
            mock_create_token.return_value = ApplicationToken(
                token='abc_token',
                expires_in=None
            )

            cmd = Command()
            cmd.handle(app='', page=1, limit=30, is_active='false')

            out, err = capsys.readouterr()

            assert 'TOKEN' in out
            assert 'abc_token' in out
