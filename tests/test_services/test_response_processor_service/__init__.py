from m3cli.services.response_processor_service import ResponseProcessorService
import unittest


class TestResponseProcessorService(unittest.TestCase):
    def setUp(self) -> None:
        self.cmd_def = {

        }
        self.view = 'json'
        self.detailed = True
        self.service = ResponseProcessorService

    def init_service_object(self):
        self.service = ResponseProcessorService(self.cmd_def, self.view,
                                                self.detailed)
