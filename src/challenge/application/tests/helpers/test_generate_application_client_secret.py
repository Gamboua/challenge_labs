from challenge.application.helpers import generate_application_client_secret


class TestGenerateApplicationClientSecret:

    def test_should_contain_64_characters(self):
        assert len(generate_application_client_secret()) == 64

    def test_should_not_generate_same_value(self):
        assert (
            generate_application_client_secret() !=
            generate_application_client_secret()
        )
