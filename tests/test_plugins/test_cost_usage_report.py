from tests.test_plugins import TestPluginsBase


class TesCostUsageReport(TestPluginsBase):
    PLUGIN_NAME = 'cost-usage-report'

    def test_cost_usage_report_json_error_response(self):
        self.response = 'some not json report'

        result = self.execute_create_custom_response()
        self.assertEqual(result, 'some not json report')

    def test_cost_usage_report_empty_response(self):
        self.response = {
            'table': {
                'message': 'error'
            }
        }

        result = self.execute_create_custom_response()
        self.assertEqual(result, 'There are no records to display')
