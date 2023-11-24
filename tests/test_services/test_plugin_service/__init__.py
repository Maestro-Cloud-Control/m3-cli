import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from m3cli.services.plugin_service import PluginService
from m3cli.utils import CONFIGURATION_FOLDER_PATH


class TestPluginService(unittest.TestCase):
    @patch.dict(os.environ, {CONFIGURATION_FOLDER_PATH: ''})
    def setUp(self) -> None:
        self.command_name = 'test_command'
        self.cmd_def = {}
        self._m3cli_path = tempfile.TemporaryDirectory()
        self.m3cli_path = self._m3cli_path.name
        os.makedirs(Path(self.m3cli_path, 'plugins'), exist_ok=True)
        self.service: PluginService

    def tearDown(self) -> None:
        self._m3cli_path.cleanup()

    def init_service_object(self):
        self.service = PluginService(self.m3cli_path, self.command_name,
                                     self.cmd_def)
