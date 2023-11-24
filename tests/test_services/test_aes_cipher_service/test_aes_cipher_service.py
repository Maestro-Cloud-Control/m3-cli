import json

from m3cli.services.aes_cipher_service import AESCipherService
from tests.test_services.test_aes_cipher_service import TestAESCipherService


class TestAESCipherServiceMethods(TestAESCipherService):
    def test_encrypt_wrong_secret_key(self):
        wrong_key = self.key + 'redundant text'
        self.service = AESCipherService(key=wrong_key)
        with self.assertRaises(ValueError) as context:
            self.service.encrypt({'param': 'value'})
        self.assertEqual(str(context.exception),
                         'Secret Key must be 128, 192, or 256 bits.')

    # todo fix tests for a new encrypt-decrypt flow on m3-server
    # def test_encrypt(self):
    #     expected_hash = 'OKxLr+CTZNGq8BsdcW+/iS1zbUCXJ6p4g2Az01RKry9gzk1' \
    #                     'fVAA162gUI4w/qhFu+ODSvg6t2NI6LV2mMlNw8EC+pHDFrp' \
    #                     '6KV3iDFAYAnIHUCM6g'
    #     result = self.service.encrypt(self.target_dict)
    #     self.assertEqual(result, expected_hash)
    #
    # def test_decrypt(self):
    #     input_hash = 'OKxLr+CTZNGq8BsdcW+/iS1zbUCXJ6p4g2Az01RKry9gzk1' \
    #                  'fVAA162gUI4w/qhFu+ODSvg6t2NI6LV2mMlNw8EC+pHDFrp' \
    #                  '6KV3iDFAYAnIHUCM6g'
    #     expected_result = b'{"data1": "some sort of data", "data2": "some ' \
    #                       b'another sort of data"}\x9ai\xa6\x97}S\xb6\xdf,' \
    #                       b'\x1d\xbd\x9b9z=\xc9'
    #     result = self.service.decrypt(input_hash)
    #     self.assertEqual(result, expected_result)

    def test_encrypt_decrypt_dict(self):
        encrypted = self.service.encrypt(self.target_dict)
        self.assertIsInstance(encrypted, str)

        decrypted = self.service.decrypt(encrypted)
        self.assertIsInstance(decrypted, bytes)

        # 'ignore' due to some salt which appears after decryption at the
        # end of the bytes string
        decrypted = decrypted.decode(errors='ignore')
        self.assertIn(json.dumps(self.target_dict, indent=None), decrypted)

    def test_encrypt_decrypt_str(self):
        target_str = json.dumps(self.target_dict)
        encrypted = self.service.encrypt(target_str)
        self.assertIsInstance(encrypted, str)

        decrypted = self.service.decrypt(encrypted)
        self.assertIsInstance(decrypted, bytes)

        decrypted = decrypted.decode(errors='ignore')
        self.assertIn(target_str, decrypted)
