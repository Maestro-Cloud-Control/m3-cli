from tests.test_plugins import TestPluginsBase


class TesCostObjectReport(TestPluginsBase):
    PLUGIN_NAME = 'cost-object-report'

    def test_cost_object_report_error_request(self):
        self.request.parameters = {
            'from': 10,
            'to': 9
        }

        with self.assertRaises(AssertionError) as context:
            self.execute_create_custom_request()
        self.assertEqual(str(context.exception), 'Parameter "from" can not be '
                                                 'equal or greater than '
                                                 'parameter "to"')

    def test_cost_object_report_request_success(self):
        self.request.parameters = {
            'tenant': 'mstr-dev2',
            'clouds': 'clouds',
            'region': 'aws-euwest',
            'productName': 'some_name',
            'usageType': 'usageType',
            'resourceType': 'resourceType',
            'from': 9,
            'to': 10
        }

        expected_result = {
            'tenant': 'mstr-dev2',
            'clouds': 'clouds',
            'reportUnit': 'TENANT_AND_RESOURCES',
            'region': 'aws-euwest',
            'productName': 'some_name',
            'usageType': 'usageType',
            'resourceType': 'resourceType'
        }

        result = self.execute_create_custom_request()
        self.assertEqual(result.parameters['target'], expected_result)

    def test_create_custom_json_error_response(self):
        self.response = 'rjklsdoi!j'

        result = self.execute_create_custom_response()
        self.assertEqual(result, 'rjklsdoi!j')
