from tests.test_plugins import TestPluginsBase


class TestDeleteTags(TestPluginsBase):
    PLUGIN_NAME = 'delete-tags'

    def test_delete_tags_resource_group_missed_request(self):
        self.request.parameters = {
            'cloud': 'AZURE'
        }

        with self.assertRaises(AssertionError) as context:
            self.execute_create_custom_request()
        self.assertEqual(str(context.exception), 'Parameter resource-group is'
                                                 ' required for AZURE cloud')

    def test_delete_tags_availability_zone_missed_request(self):
        self.request.parameters = {
            'cloud': 'GOOGLE'
        }

        with self.assertRaises(AssertionError) as context:
            self.execute_create_custom_request()
        self.assertEqual(str(context.exception), 'Parameter availability-zone'
                                                 ' is required for GOOGLE cloud')
