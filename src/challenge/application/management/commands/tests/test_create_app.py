import pytest

from challenge.application.management.commands.create_app import Command


@pytest.mark.django_db
class TestCreateAppCommand:

    def test_handle(self, capsys):
        cmd = Command()
        cmd.handle(name='fake')

        out, err = capsys.readouterr()

        assert 'fake' in out
