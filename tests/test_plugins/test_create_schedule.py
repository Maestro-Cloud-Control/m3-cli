from tests.test_plugins import TestPluginsBase


class TesCreateSchedule(TestPluginsBase):
    PLUGIN_NAME = 'create-schedule'

    def test_create_schedule_success_request(self):
        self.request.parameters = {
            'schedule': {
                'instances': ['1st', '2nd'],
                'region': 'some_region',
                'displayName': 'some_name',
                'scheduleType': 'some_type',
                'tagKey': 'some_tag',
                'tagValue': 'some_value'
            }
        }

        expected_result = {
            'schedule': {
                'instances': [
                    {
                        'instanceId': '1st',
                        'instanceLocationInfo': {
                            'region': 'some_region'
                        }
                    },
                    {
                        'instanceId': '2nd',
                        'instanceLocationInfo': {
                            'region': 'some_region'
                        }
                    }
                ],
                'region': 'some_region',
                'displayName': 'some_name',
                'scheduleType': 'some_type',
                'whenToExecute': 'By cron expression',
                'scheduleName': 'some_name::some_region',
                'tag': {
                    'key': 'some_tag', 'value': 'some_value'
                }
            }
        }

        result = self.execute_create_custom_request()
        self.assertEqual(result.parameters, expected_result)

    def test_create_schedule_missed_parameters_error_request(self):
        self.request.parameters = {
            'schedule': {
                'instances': ['1st', '2nd'],
                'region': 'some_region',
                'displayName': 'some_name',
                'scheduleType': 'My instances with tag'
            }
        }

        with self.assertRaises(AssertionError) as context:
            self.execute_create_custom_request()
        self.assertEqual(str(context.exception),
                         'Parameters "tagKey" and "tagValue" are required '
                         'for schedule type "My instances with tag"')
