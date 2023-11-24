import unittest

from m3cli.services.response_utils import contains_string_data, \
    contains_dict_data, contains_empty_data


class TestContainsStringData(unittest.TestCase):
    def test_contains_string_data_success(self):
        self.assertTrue(contains_string_data(['string', ]))

    def test_contains_string_data_fail(self):
        self.assertFalse(contains_string_data(['string1', 'string2']))
        self.assertFalse(contains_string_data([1, ]))
        self.assertFalse(contains_string_data([1, 'string']))
        self.assertFalse(contains_string_data([{'key': 'value'}]))


class TestContainsDictData(unittest.TestCase):
    def test_contains_dict_data_success(self):
        self.assertTrue(contains_dict_data([{'key': 'value'}, ]))
        self.assertTrue(contains_dict_data([{}, ]))

    def test_contains_dict_data_fail(self):
        self.assertFalse(contains_dict_data([{}, {}]))
        self.assertFalse(contains_dict_data(['string', {'key': 'value'}]))
        self.assertFalse(contains_dict_data([{'key', 'value'}]))
        self.assertFalse(contains_dict_data([1, 2]))


class TestContainsEmptyData(unittest.TestCase):
    def test_contains_empty_data_success(self):
        self.assertTrue(contains_empty_data([{}]))
        self.assertTrue(contains_empty_data([[]]))
        self.assertTrue(contains_empty_data([None]))
        self.assertTrue(contains_empty_data(['']))
        self.assertTrue(contains_empty_data({}))
        self.assertTrue(contains_empty_data([]))
        self.assertTrue(contains_empty_data(''))
        self.assertTrue(contains_empty_data(None))

    def test_contains_empty_data_fail(self):
        self.assertFalse(contains_empty_data([1, ]))
        self.assertFalse(contains_empty_data([{'key': 'value'}]))
        self.assertFalse(contains_empty_data(['string', ]))
