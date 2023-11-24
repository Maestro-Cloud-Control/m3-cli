import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from m3cli.services.environment_service import _get_certain_credential
from m3cli.services.environment_service import _get_credentials_from_file
from m3cli.utils import CREDENTIALS_FILE


class TestEnvironmentServiceMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.secret_name, self.secret_value = 'name', 'value'
        self._m3_cli_resources_path = tempfile.TemporaryDirectory()
        self.m3_cli_resource_path = self._m3_cli_resources_path.name
        self.credentials_file_path = str(Path(self.m3_cli_resource_path,
                                              CREDENTIALS_FILE))
        with open(self.credentials_file_path, 'w') as file:
            json.dump({self.secret_name: self.secret_value}, file)
        self.resource_path_patch = patch(
            'm3cli.services.environment_service.M3_CLI_RESOURCES_PATH',
            self.m3_cli_resource_path)
        self.credentials_file_path_patch = patch(
            'm3cli.services.environment_service.CREDENTIALS_FILE_PATH',
            self.credentials_file_path)
        self.resource_path_patch.start()
        self.credentials_file_path_patch.start()

    def tearDown(self) -> None:
        self.resource_path_patch.stop()
        self.credentials_file_path_patch.stop()
        self._m3_cli_resources_path.cleanup()

    def test_get_credentials_from_file(self):
        result = _get_credentials_from_file(self.secret_name)
        self.assertEqual(result, self.secret_value)

    def test_get_certain_credential_key_exists(self):
        result = _get_certain_credential(self.secret_name)
        self.assertEqual(result, self.secret_value)

    def test_get_certain_credential_key_from_env(self):
        another_name, another_value = 'another_name', 'another_value'
        with patch.dict(os.environ, {another_name: another_value}):
            result = _get_certain_credential(another_name)
        self.assertEqual(result, another_value)
