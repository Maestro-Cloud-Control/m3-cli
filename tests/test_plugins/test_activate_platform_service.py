from tests.test_plugins import TestPluginsBase


class TestActivatePlatformService(TestPluginsBase):
    PLUGIN_NAME = 'activate-platform-service'

    def test_activate_platform_service_response_success(self):
        self.response = {
            'id': 'test_id',
            'creationDate': 1642610237037.19  # from java
        }
        expected_result = {
            'serviceId': 'test_id',
            'creationDate': '2022-01-19T16:37:17+00:00'
        }
        result = self.execute_create_custom_response()
        self.assertEqual(result, expected_result)

    def test_activate_platform_service_response_invalid_json(self):
        self.response = "{'id': 'test_id'}"
        result = self.execute_create_custom_response()
        self.assertEqual(result, self.response)
