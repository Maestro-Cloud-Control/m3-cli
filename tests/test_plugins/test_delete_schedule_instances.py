import os
from tests.test_plugins import TestPluginsBase


class TestDeleteScheduleInstances(TestPluginsBase):
    PLUGIN_NAME = 'delete-schedule-instances'

    def test_delete_schedule_instances_json_decode_error_response(self):
        self.response = 'error or else'

        result = self.execute_create_custom_response()
        self.assertEqual(result, 'error or else')

    def test_delete_schedule_instances_success_response(self):
        self.response = '[{"success": 200}]'

        result = self.execute_create_custom_response()
        self.assertEqual(result, 'Instances were removed from the schedule.')

    def test_delete_schedule_instances_failed_response(self):
        self.response = '[{"failed": 500, "reason": "some_reason"}]'

        result = self.execute_create_custom_response()
        self.assertEqual(result, 'Instances were not removed from the '
                                 f'schedule.{os.linesep}Reason: some_reason')

    def test_delete_schedule_instances_table_response(self):
        self.response = '[{"failed": 500, "reason": "some_reason"},' \
                        '{"success": 200}]'

        expected_result = [{'Instance': None, 'Status': 'Removed'},
                           {'Instance': None, 'Status': 'Not removed',
                            'Reason': 'some_reason'}]

        result = self.execute_create_custom_response()
        self.assertEqual(result, expected_result)
