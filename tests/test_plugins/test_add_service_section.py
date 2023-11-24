import os
import tempfile

from m3cli.services.request_service import BaseRequest
from tests.test_plugins import TestPluginsBase


class TestAddServiceSection(TestPluginsBase):
    PLUGIN_NAME = 'add-service-section'

    def test_add_service_section_request_params_not_specified(self):
        self.request = BaseRequest(self.command, parameters={})

        with self.assertRaises(AssertionError) as context:
            self.execute_create_custom_request()
        self.assertEqual(str(context.exception),
                         "One of the 'block-value' and 'block-value-path' "
                         "parameters must be specified")

    def test_add_service_section_request_success(self):
        parameters = {'blockValue': 'value'}
        self.request = BaseRequest(self.command, parameters=parameters)
        result = self.execute_create_custom_request()
        self.assertEqual(result.parameters, parameters)

    def test_add_service_section_request_load_from_file(self):
        value = 'value'
        expected_parameters = {
            'blockValue': value
        }
        file = tempfile.NamedTemporaryFile(delete=False)
        file.write(value.encode())
        file.close()
        self.request = BaseRequest(self.command, parameters={
            'blockValuePath': file.name
        })
        result = self.execute_create_custom_request()
        self.assertEqual(result.parameters, expected_parameters)
        if os.path.exists(file.name):
            os.remove(file.name)
