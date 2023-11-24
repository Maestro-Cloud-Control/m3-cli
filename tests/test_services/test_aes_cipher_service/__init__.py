import unittest

from m3cli.services.aes_cipher_service import AESCipherService


class TestAESCipherService(unittest.TestCase):
    def setUp(self) -> None:
        self.target_dict = {
            'data1': 'some sort of data',
            'data2': 'some another sort of data'
        }
        self.key = 'I"m strong secret key, aren"t I?'
        self.service = AESCipherService(key=self.key)
