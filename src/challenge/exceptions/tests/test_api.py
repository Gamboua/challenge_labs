import pytest

from challenge.exceptions.api import APIException


class TestApiException:

    @pytest.fixture
    def api_exception(self):
        return APIException()

    def test_should_be_instance_from_exception(self, api_exception):
        assert isinstance(api_exception, Exception)

    def test_should_return_status_code_500_by_default(self, api_exception):
        assert api_exception.status_code == 500

    def test_should_return_default_code_in_detail(self, api_exception):
        full_detail = api_exception.get_full_details()
        assert full_detail['code'] == 'server_error'

    def test_should_return_specific_code_in_detail(self):
        api_exception = APIException(code='specific_code')
        full_detail = api_exception.get_full_details()
        assert full_detail['code'] == 'specific_code'

    def test_should_return_default_message_in_detail(self, api_exception):
        full_detail = api_exception.get_full_details()
        assert full_detail['message'] == 'A server error occured.'

    def test_should_return_specific_message_in_detail(self):
        api_exception = APIException(message='specifc message')
        full_detail = api_exception.get_full_details()
        assert full_detail['message'] == 'specifc message'

    def test_should_return_empty_details(self, api_exception):
        full_detail = api_exception.get_full_details()
        assert full_detail['details'] is None

    def test_should_return_details(self):
        api_exception = APIException(details='specifc detail')
        full_detail = api_exception.get_full_details()
        assert full_detail['details'] == 'specifc detail'
