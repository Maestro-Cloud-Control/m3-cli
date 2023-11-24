from tests.test_plugins import TestPluginsBase


class TestAzureManagementConsole(TestPluginsBase):
    PLUGIN_NAME = 'azure-management-console'

    def test_azure_management_console_request(self):
        self.request.parameters = {
            'cloud': 'anything',
            'accessType': 'anything'
        }

        expected_result = {
            'cloud': 'AZURE',
            'accessType': 'DEFAULT'
        }

        result = self.execute_create_custom_request()
        self.assertEqual(result.parameters, expected_result)

    def test_azure_management_console_null_response(self):
        self.response = 'null'

        expected_result = 'The letter with console credentials was ' \
                          'successfully sent'

        result = self.execute_create_custom_response()
        self.assertEqual(result, expected_result)

    def test_azure_management_console_else_response(self):
        self.response = 'Some problem or another answer from server'

        expected_result = 'Some problem or another answer from server'

        result = self.execute_create_custom_response()
        self.assertEqual(result, expected_result)
