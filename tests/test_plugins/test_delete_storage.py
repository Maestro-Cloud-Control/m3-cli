from tests.test_plugins import TestPluginsBase


class TestDeleteStorage(TestPluginsBase):
    PLUGIN_NAME = 'delete-storage'

    def test_delete_storage_success_request(self):
        self.request.parameters = {
            'region': 'AZURE'
        }

        expected_result = {
            'region': 'AZURE',
            'params': {}
        }

        result = self.execute_create_custom_request()
        self.assertEqual(result.parameters, expected_result)

    def test_delete_storage_availability_zone_missed_request(self):
        self.request.parameters = {
            'region': 'GCP'
        }

        with self.assertRaises(AssertionError) as context:
            self.execute_create_custom_request()
        self.assertEqual(str(context.exception), 'Parameter availability-zone '
                                                 'is required for GOOGLE cloud')
