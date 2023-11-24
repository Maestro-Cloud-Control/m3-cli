from tests.test_plugins import TestPluginsBase


class TestDeleteServiceSection(TestPluginsBase):
    PLUGIN_NAME = 'delete-service-section'

    def test_delete_service_section_success_request(self):
        self.request.parameters = {
            'deleteBlockWithoutTitle': 'some_title'
        }

        expected_result = {
            'deleteBlockWithoutTitle': True,
            'deleteAllBlocks': False,
            'blockTitle': ''
        }

        result = self.execute_create_custom_request()
        self.assertEqual(result.parameters, expected_result)

    def test_delete_service_section_error_request(self):
        self.request.parameters = {
            'deleteBlockWithoutTitle': True,
            'deleteAllBlocks': True
        }

        with self.assertRaises(AssertionError) as context:
            self.execute_create_custom_request()
        self.assertEqual(str(context.exception),
                         "Specify only one of the following parameters: "
                         "'--block-title', "
                         "'--delete-all', '--delete-empty' ")
