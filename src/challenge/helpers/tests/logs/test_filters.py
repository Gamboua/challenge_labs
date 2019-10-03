import socket
from unittest.mock import Mock

import pytest

from challenge.helpers.logs.filters import AddHostName, NotIncludeHealthcheck


class TestAddHostName:

    @pytest.fixture
    def hostname_filter(self):
        return AddHostName()

    def test_filter_should_add_a_hostname_to_the_given_record(
        self,
        hostname_filter
    ):
        record = Mock()
        hostname_filter.filter(record)

        assert record.hostname == socket.gethostname()

    def test_filter_should_return_true(self, hostname_filter):
        record = Mock()
        assert hostname_filter.filter(record)


class TestNotIncludeHealthcheck:

    @pytest.fixture
    def hostname_filter(self):
        return NotIncludeHealthcheck()

    def test_filter_healthcheck_log(
        self,
        hostname_filter
    ):
        record = Mock()
        record.getMessage.return_value = 'GET /healthcheck/'

        assert hostname_filter.filter(record) is False

    def test_filter_by_not_healthcheck_log(self, hostname_filter):
        record = Mock()
        record.getMessage.return_value = 'GET /shipping/'
        assert hostname_filter.filter(record) is True
