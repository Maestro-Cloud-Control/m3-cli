from tests.test_plugins import TestPluginsBase


class TestCreateKey(TestPluginsBase):
    PLUGIN_NAME = 'create-key'

    def test_create_key_success_request(self):
        self.request.parameters = {
            'allTenants': True
        }

        expected_result = {
            'allTenants': True
        }

        result = self.execute_create_custom_request()
        self.assertEqual(result.parameters, expected_result)

    def test_create_key_tenant_name_and_parameter_error_request(self):
        self.request.parameters = {}

        with self.assertRaises(AssertionError) as context:
            self.execute_create_custom_request()
        self.assertEqual(str(context.exception),
                         "Please specify at least one of the following "
                         "parameters: '--tenant' or '--all-tenants'")

    def test_create_key_all_tenants_and_region_error_request(self):
        self.request.parameters = {
            'allTenants': True,
            'region': 'some_region'
        }

        with self.assertRaises(AssertionError) as context:
            self.execute_create_custom_request()
        self.assertEqual(str(context.exception),
                         "The '--region' parameter is not allowed "
                         "when '--all-tenants' specified")

    def test_create_key_all_cloud_and_region_error_request(self):
        self.request.parameters = {
            'tenantName': 'some_name'
        }

        with self.assertRaises(AssertionError) as context:
            self.execute_create_custom_request()
        self.assertEqual(str(context.exception),
                         "The tenantName parameter(s) should be specified "
                         "with the following parameter(s): cloud, region")
