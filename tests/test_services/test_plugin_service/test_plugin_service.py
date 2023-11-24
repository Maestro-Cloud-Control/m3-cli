from pathlib import Path
from unittest.mock import MagicMock

from m3cli.services.plugin_service import INTEGRATION_SUFFIX_ATTRIBUTE_NAME
from tests.test_services.test_plugin_service import TestPluginService


class TestPluginServiceInit(TestPluginService):
    def test_init(self):
        self.init_service_object()
        self.assertEqual(self.service.command_name, self.command_name)
        self.assertEqual(self.service.cmd_def, self.cmd_def)
        self.assertEqual(self.service.built_in_plugins_path,
                         str(Path(self.m3cli_path, 'plugins')))

    def test_init_with_integration_suffix(self):
        suffix = 'suffix'
        self.cmd_def = {
            INTEGRATION_SUFFIX_ATTRIBUTE_NAME: suffix
        }
        self.init_service_object()
        self.assertEqual(self.service.command_name,
                         f'{self.command_name}-{suffix}')


class TestPluginServiceApplyPlugin(TestPluginService):
    def setUp(self) -> None:
        super().setUp()
        self.request_data = 'request_data'
        self.response_data = 'response_data'
        self.data = {
            'request': self.request_data,
            'response': self.response_data
        }
        self.cmd_def = {
            'integration_request': True,
            'integration_response': True
        }
        self.init_service_object()
        self.plugin_return_value = 'return'
        self.plugin_method = MagicMock(return_value=self.plugin_return_value)
        self.service.validate_method = MagicMock(
            return_value=self.plugin_method)

    def test_apply_plugin_not_method_type_request(self):
        method_type = 'integration_request'
        self.cmd_def = {
            method_type: False
        }
        self.init_service_object()
        result = self.service.apply_plugin(self.data, method_type)
        self.assertEqual(result, self.request_data)

    def test_apply_plugin_not_method_type_response(self):
        method_type = 'integration_response'
        self.cmd_def = {
            method_type: False
        }
        self.init_service_object()
        result = self.service.apply_plugin(self.data, method_type)
        self.assertEqual(result, self.response_data)

    def test_apply_plugin_success_request(self):
        result = self.service.apply_plugin(self.data, 'integration_request')
        self.service.validate_method.assert_called_with(
            method='create_custom_request')
        self.plugin_method.assert_called_with(self.request_data)
        self.assertEqual(result, self.plugin_return_value)

    def test_apply_plugin_success_response(self):
        result = self.service.apply_plugin(self.data, 'integration_response')
        self.service.validate_method.assert_called_with(
            method='create_custom_response')
        self.plugin_method.assert_called_with(self.request_data,
                                              self.response_data)
        self.assertEqual(result, self.plugin_return_value)
