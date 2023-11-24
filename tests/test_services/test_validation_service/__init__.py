import unittest

from m3cli.services.validation_service import ValidationService


class TestValidationService(unittest.TestCase):
    def setUp(self) -> None:
        self.service = ValidationService()


class TestValidationServiceCheck(TestValidationService):
    """Contains commons for 'check_{type}' methods and some others which
    take 'param_name' and 'validation_rules' params"""
    def setUp(self) -> None:
        super().setUp()
        self.param_name = 'param_name'
        self.validation_rules = {}
