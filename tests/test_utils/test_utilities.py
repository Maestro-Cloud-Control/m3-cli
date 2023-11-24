import json
import os.path
import tempfile
import unittest

from m3cli.utils.utilities import \
    __write_credentials_to_file as write_credentials_to_file
from m3cli.utils.utilities import inherit_dict
from m3cli.utils.utilities import is_not_empty_file
from m3cli.utils.utilities import timestamp_to_iso


class TestInheritDict(unittest.TestCase):
    def test_inherit_dict_not_root(self):
        child_dict = {'key': 'value'}
        result = inherit_dict({}, child_dict)
        self.assertEqual(result, child_dict)

    def test_inherit_dict(self):
        root_dict = {'key1': 'value1', 'key2': 'value2'}
        child_dict = {'key1': 'new_value1'}
        expected_result = {'key1': 'new_value1', 'key2': 'value2'}
        result = inherit_dict(root_dict, child_dict)
        self.assertEqual(result, expected_result)


class TestWriteCredentialsToFile(unittest.TestCase):
    def setUp(self) -> None:
        self.access_key, self.secret_key = 'access_key', 'secret_key'
        self.api_address = 'api_address'
        self._credentials_path = tempfile.NamedTemporaryFile(delete=False)
        self.credentials_path = self._credentials_path.name
        self._credentials_path.close()

    def tearDown(self) -> None:
        if os.path.exists(self.credentials_path):
            os.remove(self.credentials_path)

    def test_write_credentials_to_file_exists_invalid_json(self):
        invalid_json = '{\'key\': "value"}'
        with open(self.credentials_path, 'w') as file:
            file.write(invalid_json)
        with self.assertRaises(SyntaxError) as context:
            write_credentials_to_file(self.credentials_path, self.access_key,
                                      self.secret_key, self.api_address)
        self.assertEqual(str(context.exception),
                         f'{self.credentials_path} contains invalid JSON')

    def test_write_credentials_to_file_exists_valid_json(self):
        valid_json = '{"key": "value"}'
        with open(self.credentials_path, 'w') as file:
            file.write(valid_json)
        write_credentials_to_file(self.credentials_path, self.access_key,
                                  self.secret_key, self.api_address)

        with open(self.credentials_path, 'r') as file:
            data = json.load(file)
        expected_data = {
            'key': 'value',
            'M3SDK_ACCESS_KEY': self.access_key,
            'M3SDK_SECRET_KEY': self.secret_key,
            'M3SDK_ADDRESS': self.api_address
        }
        self.assertEqual(data, expected_data)

    def test_write_credentials_to_file_does_not_exist(self):
        os.remove(self.credentials_path)
        write_credentials_to_file(self.credentials_path, self.access_key,
                                  self.secret_key, self.api_address)
        with open(self.credentials_path, 'r') as file:
            data = json.load(file)
        expected_data = {
            'M3SDK_ACCESS_KEY': self.access_key,
            'M3SDK_SECRET_KEY': self.secret_key,
            'M3SDK_ADDRESS': self.api_address
        }
        self.assertEqual(data, expected_data)


class TestIsNotEmptyFile(unittest.TestCase):
    def setUp(self) -> None:
        self._file = tempfile.NamedTemporaryFile(delete=False)
        self.file = self._file.name
        self._file.close()

    def tearDown(self) -> None:
        if os.path.exists(self.file):
            os.remove(self.file)

    def test_is_not_empty_file_false(self):
        self.assertFalse(is_not_empty_file(self.file))

    def test_is_not_empty_file_true(self):
        with open(self.file, 'w') as file:
            file.write('1')
        self.assertTrue(is_not_empty_file(self.file))


class TestTimestampToIso(unittest.TestCase):
    def test_timestamp_to_iso(self):
        timestamp = 1643815854797.82
        expected_iso = '2022-02-02T15:30:54+00:00'
        result = timestamp_to_iso(timestamp)
        self.assertEqual(result, expected_iso)
