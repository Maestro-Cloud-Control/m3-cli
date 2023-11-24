import importlib
import json
import unittest
from typing import Union

from m3cli.services.plugin_service import INTEGRATION_REQUEST_METHOD_NAME, \
    INTEGRATION_RESPONSE_METHOD_NAME
from m3cli.services.request_service import BaseRequest


class TestPluginsBase(unittest.TestCase):
    PLUGIN_NAME = None

    def setUp(self) -> None:
        self.command = 'test_command'
        self.request: BaseRequest = BaseRequest(command=self.command)
        self.response: Union[str, dict] = {}
        if not self.PLUGIN_NAME:
            raise AssertionError('\'PLUGIN_NAME\' class variable must be set')
        self.plugin = importlib.import_module(
            f'm3cli.plugins.{self.PLUGIN_NAME}')

    def execute_create_custom_request(self) -> BaseRequest:
        if not hasattr(self.plugin, INTEGRATION_REQUEST_METHOD_NAME):
            raise AssertionError(
                f'Plugin: \'{self.plugin}\' does not have '
                f'\'{INTEGRATION_REQUEST_METHOD_NAME}\' implemented')
        return getattr(self.plugin, INTEGRATION_REQUEST_METHOD_NAME)(
            self.request)

    def execute_create_custom_response(self) -> dict:
        if not hasattr(self.plugin, INTEGRATION_RESPONSE_METHOD_NAME):
            raise AssertionError(
                f'Plugin: \'{self.plugin}\' does not have '
                f'\'{INTEGRATION_REQUEST_METHOD_NAME}\' implemented')
        if isinstance(self.response, dict):
            response = json.dumps(self.response)
        elif isinstance(self.response, str):
            response = self.response
        else:
            raise TypeError('\'self.response\' must either str or dict')
        return getattr(self.plugin, INTEGRATION_RESPONSE_METHOD_NAME)(
            self.request, response)
