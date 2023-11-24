from tests.test_plugins import TestPluginsBase


class TestCreateInstanceQuota(TestPluginsBase):
    PLUGIN_NAME = 'create-instance-quota'

    def test_create_instance_quota_request(self):
        self.request.parameters = {
            'creationIntervalCount': 10,
            'creationIntervalHours': 10
        }

        expected_result = {
            'instanceQuota': {
                'creationIntervalCount': 10,
                'creationIntervalHours': 10
            }
        }

        result = self.execute_create_custom_request()
        self.assertEqual(result.parameters, expected_result)
