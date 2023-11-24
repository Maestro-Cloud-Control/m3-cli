import unittest

from m3cli.services.interactivity.interactive_input_service import \
    InteractiveInputService
from m3cli.services.interactivity.parameters_provider import ParametersProvider
from m3cli.services.interactivity.remote_validation_service import \
    RemoteValidationService
from m3cli.services.interactivity.varfile.varfile_service import VarfileService


class TestVarfileService(unittest.TestCase):
    def setUp(self) -> None:
        self.interactive_options = {}
        self.service = VarfileService(self.interactive_options)


class TestInteractiveInputService(unittest.TestCase):
    def setUp(self) -> None:
        self.interactive_options = {}
        self.service = InteractiveInputService

    def init_service_object(self):
        self.service = InteractiveInputService(self.interactive_options)


class TestParametersProvider(unittest.TestCase):
    def setUp(self) -> None:
        self.api_action = 'API_ACTION'
        self.interactive_option = {'parameters_handler': self.api_action}
        self.service = ParametersProvider(self.interactive_option)


class TestRemoteValidationService(unittest.TestCase):
    def setUp(self) -> None:
        self.api_action = 'API_ACTION'
        self.interactive_option = {'validation_handler': self.api_action}
        self.service = RemoteValidationService

    def init_service_object(self):
        self.service = RemoteValidationService(self.interactive_option)
