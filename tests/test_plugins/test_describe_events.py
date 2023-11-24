from tests.test_plugins import TestPluginsBase


class TestDescribeEvents(TestPluginsBase):
    PLUGIN_NAME = 'describe-events'

    def test_describe_events_success_request(self):
        self.request.parameters = {
            'cloud': 'AWS',
            'region': 'aws-eucentral'
        }

        expected_result = {
            'count': 10,
            'cloud': 'AWS',
            'region': 'aws-eucentral'
        }

        result = self.execute_create_custom_request()
        self.assertEqual(result.parameters, expected_result)

    def test_describe_events_assertion_error_request(self):
        self.request.parameters = {
            'cloud': 'AWS',
            'region': 'aws-eucentral',
            'searchType': 'RELATED'
        }

        with self.assertRaises(AssertionError) as context:
            self.execute_create_custom_request()
        self.assertEqual(str(context.exception),
                         "The `--resource-id` parameter is"
                         " required in case the RELATED "
                         "search-type is specified")
