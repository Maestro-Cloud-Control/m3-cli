from tests.test_plugins import TestPluginsBase


class TestDescribePlatformServices(TestPluginsBase):
    PLUGIN_NAME = 'describe-platform-services'

    def test_describe_platform_services_success_request(self):
        self.request.parameters = {
            'serviceName': 'service'
        }

        expected_result = {
            'serviceName': 'service'
        }

        result = self.execute_create_custom_request()
        self.assertEqual(result.parameters, expected_result)

    def test_describe_platform_services_no_specified_error_request(self):
        self.request.parameters = {
            'platform': 'some_platform'
        }

        with self.assertRaises(AssertionError) as context:
            self.execute_create_custom_request()
        self.assertEqual(str(context.exception), "Specify only one of the "
                                                 "following groups of the "
                                                 "parameters: "
                                                 "1. '--cloud' and '--tenant';"
                                                 " 2. '--service' ")

    def test_describe_platform_services_no_specified_cloud_error_request(self):
        self.request.parameters = {
            'platform': 'some_platform',
            'tenantName': 'some_tenant'
        }

        with self.assertRaises(AssertionError) as context:
            self.execute_create_custom_request()
        self.assertEqual(str(context.exception),
                         "The '--cloud' and '--tenant' "
                         "parameters are required if "
                         "'--service' is empty and vice versa")
