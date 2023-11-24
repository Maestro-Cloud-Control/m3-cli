from tests.test_plugins import TestPluginsBase


class TestDeleteStorage(TestPluginsBase):
    PLUGIN_NAME = 'delete-storage'

    def test_delete_storage_success_request(self):
        self.request.parameters = {
            'region': 'AZURE',
            'resourceGroup': 'some_group'
        }

        expected_result = {
            'region': 'AZURE',
            'resourceGroup': 'some_group',
            'params': {
                'resourceGroupName': 'some_group'
            }
        }

        result = self.execute_create_custom_request()
        self.assertEqual(result.parameters, expected_result)

    def test_delete_storage_resource_group_missed_request(self):
        self.request.parameters = {
            'region': 'AZURE'
        }

        with self.assertRaises(AssertionError) as context:
            self.execute_create_custom_request()
        self.assertEqual(str(context.exception), 'Parameter resource-group'
                                                 ' is required for AZURE cloud')

    def test_delete_storage_availability_zone_missed_request(self):
        self.request.parameters = {
            'region': 'GCP'
        }

        with self.assertRaises(AssertionError) as context:
            self.execute_create_custom_request()
        self.assertEqual(str(context.exception), 'Parameter availability-zone '
                                                 'is required for GOOGLE cloud')
