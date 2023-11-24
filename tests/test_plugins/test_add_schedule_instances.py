import os
from tests.test_plugins import TestPluginsBase


class TestAddScheduleInstances(TestPluginsBase):
    PLUGIN_NAME = 'add-schedule-instances'

    def test_add_schedule_instances_json_decode_error_response(self):
        self.response = 'error or else'

        result = self.execute_create_custom_response()
        self.assertEqual(result, 'error or else')

    def test_add_schedule_instances_success_response(self):
        self.response = '[{"success": 200}]'

        result = self.execute_create_custom_response()
        self.assertEqual(result, 'Instances were added to the schedule.')

    def test_add_schedule_instances_failed_response(self):
        self.response = '[{"failed": 500, "reason": "some_reason"}]'

        result = self.execute_create_custom_response()
        self.assertEqual(result, 'Instances were not added to the '
                                 f'schedule.{os.linesep}Reason: some_reason')

    def test_add_schedule_instances_table_response(self):
        self.response = '[{"failed": 500, "reason": "some_reason"},' \
                        '{"success": 200}]'

        expected_result = [{'Instance': None, 'Status': 'Added'},
                           {'Instance': None, 'Status': 'Not added',
                            'Reason': 'some_reason'}]

        result = self.execute_create_custom_response()
        self.assertEqual(result, expected_result)
