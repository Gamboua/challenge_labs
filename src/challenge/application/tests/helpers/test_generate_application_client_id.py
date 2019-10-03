from challenge.application.helpers import generate_application_client_id


class TestGenerateApplicationClientId:

    def test_should_contain_32_characters(self):
        assert len(generate_application_client_id()) == 32

    def test_should_not_generate_same_value(self):
        assert (
            generate_application_client_id() !=
            generate_application_client_id()
        )
