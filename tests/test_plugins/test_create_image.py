from tests.test_plugins import TestPluginsBase


class TesCreateImage(TestPluginsBase):
    PLUGIN_NAME = 'create-image'

    def test_create_image_json_error_response(self):
        self.response = '[]'

        result = self.execute_create_custom_response()
        self.assertEqual(result, '[]')
