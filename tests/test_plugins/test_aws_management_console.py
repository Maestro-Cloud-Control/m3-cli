from tests.test_plugins import TestPluginsBase


class TestAwsManagementConsole(TestPluginsBase):
    PLUGIN_NAME = 'aws-management-console'

    def test_aws_management_console_response_success(self):
        self.response = 'null'

        expected_result = 'The letter with console credentials was ' \
                          'successfully sent'

        result = self.execute_create_custom_response()
        self.assertEqual(result, expected_result)

    def test_aws_management_console_response_else(self):
        self.response = 'anything else'

        expected_result = 'anything else'

        result = self.execute_create_custom_response()
        self.assertEqual(result, expected_result)

    def test_aws_management_console_request(self):
        self.request.parameters = {
            'cloud': 'AZURE'
        }

        result = self.execute_create_custom_request()
        self.assertEqual(result.parameters['cloud'], 'AWS')
