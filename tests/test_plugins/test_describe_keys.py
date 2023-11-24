from tests.test_plugins import TestPluginsBase


class TestDescribeKeys(TestPluginsBase):
    PLUGIN_NAME = 'describe-keys'

    def test_describe_keys_success_request(self):
        self.request.parameters = {
            'name': 'some_name'
        }

        expected_parameters = {
            'name': 'some_name'
        }

        result = self.execute_create_custom_request()
        self.assertEqual(result.parameters, expected_parameters)

    def test_describe_keys_assertion_error_request(self):
        self.request.parameters = {
            'key': 'some_key'
        }

        with self.assertRaises(AssertionError) as context:
            self.execute_create_custom_request()
        self.assertEqual(str(context.exception),
                         'Please specified one of the following '
                         'parameters: region, tenant, cloud or key name')
