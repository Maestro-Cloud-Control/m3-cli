from tests.test_plugins import TestPluginsBase


class TestDeactivatePlatformService(TestPluginsBase):
    PLUGIN_NAME = 'deactivate-platform-service'

    def test_deactivate_platform_service_response(self):

        result = self.execute_create_custom_response()
        self.assertEqual(result, "The request to deactivate platform service "
                                 "was successfully sent")
