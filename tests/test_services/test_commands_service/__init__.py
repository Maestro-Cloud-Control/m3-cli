import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from m3cli.services.commands_service import CommandsService, \
    COMMANDS_DEF_FILE_NAME
from m3cli.services.validation_service import ValidationService
from m3cli.utils import CONFIGURATION_FOLDER_PATH


class TestCommandsService(unittest.TestCase):
    DEFAULT_PARAMETERS = json.dumps({
        'key1': 'value1'
    })
    COMMANDS_DEF = json.dumps({
        "groups": [],
        "domain_parameters": {},
        "commands": {},
        "version": "1"
    })

    def setUp(self) -> None:
        self._m3cli_path = tempfile.TemporaryDirectory()
        self._default_cr_path = tempfile.NamedTemporaryFile(delete=False)
        self.m3cli_path = self._m3cli_path.name
        self.default_cr_path = self._default_cr_path.name
        self._default_cr_path.close()

        self.validation_service = ValidationService()
        self.service = CommandsService

    def tearDown(self) -> None:
        self._m3cli_path.cleanup()
        if os.path.exists(self.default_cr_path):
            os.remove(self.default_cr_path)

    @patch.dict(os.environ, {CONFIGURATION_FOLDER_PATH: ""})
    def init_service_object(self):
        """Creates a new commands service object with DEFAULT_PARAMETERS and
        COMMANDS_DEF class attributes"""
        with open(Path(self.m3cli_path, COMMANDS_DEF_FILE_NAME), 'w') as file:
            file.write(self.COMMANDS_DEF)
        with open(self.default_cr_path, 'w') as file:
            file.write(self.DEFAULT_PARAMETERS)
        with patch('m3cli.services.commands_service._resolve_default_cr_path',
                   return_value=self.default_cr_path):
            self.service = CommandsService(self.m3cli_path,
                                           self.validation_service)
