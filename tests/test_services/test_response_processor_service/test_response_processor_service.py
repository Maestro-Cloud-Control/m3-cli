import os
import unittest
from copy import deepcopy
from unittest.mock import MagicMock, patch

from m3cli.services.response_processor_service import READABLE_ERROR_FILED, \
    ERROR_FILED, STATUS, DATA_FIELD, HEADER_DISPLAY_NAME, FULL_VIEW
from m3cli.services.response_processor_service import TableDataContainer
from m3cli.services.response_processor_service import TableView
from m3cli.services.response_processor_service import _camel_to_title
from m3cli.services.response_processor_service import \
    _change_header_display_name
from m3cli.services.response_processor_service import \
    _configure_table_response
from m3cli.services.response_processor_service import _format_lists
from m3cli.services.response_processor_service import \
    _resolve_disable_numparse_indices
from m3cli.services.response_processor_service import \
    _resolve_header_display_name
from tests.test_services.test_response_processor_service import \
    TestResponseProcessorService


class TestFormatLists(unittest.TestCase):
    def test_format_lists(self):
        responses = [
            [
                {
                    'item1': ['value2', 'value1'],
                    'key1': 'not a list',
                    'key2': ['next not a string', 1]
                }
            ],
            {
                'item2': ['value4', 'value3']
            }
        ]
        headers_config = {
            'item2': {
                'prevent_list_formatting': True
            }
        }
        expected_result = deepcopy(responses)
        expected_result[0][0]['item1'] = 'value1\nvalue2'
        result = _format_lists(responses, headers_config)
        self.assertEqual(result, expected_result)


class TestConfigureTableResponses(unittest.TestCase):
    def setUp(self) -> None:
        self.responses = [
            [
                {'headerOne': 'data'},
            ],
            {'headerTwo': 'data'}
        ]
        self.response_table_headers = ['headerOne', 'headerTwo']

    def test_configure_table_responses_not_list(self):
        responses = {'header1': 'data'}
        result = _configure_table_response(responses,
                                           self.response_table_headers)
        self.assertEqual(result, (responses, self.response_table_headers))

    def test_configure_table_responses(self):
        expected_responses = [
            [
                {'Header One': 'data'},
            ],
            {'Header Two': 'data'}
        ]
        result = _configure_table_response(self.responses,
                                           self.response_table_headers)
        self.assertEqual(result[0], expected_responses)
        self.assertEqual(result[1], ['Header One', 'Header Two'])


class TestChangeHeaderDisplayName(unittest.TestCase):
    def setUp(self) -> None:
        self.header, self.custom_header = 'header_to_change', 'replacement'

    def test_change_header_display_name_list(self):
        responses = [
            [
                {self.header: 'data'},
                {self.header: False},
                {'not_to_change': 'data'}
            ],
            {self.header: None}
        ]
        expected_responses = [
            [
                {self.custom_header: 'data'},
                {self.custom_header: False},
                {'not_to_change': 'data'}
            ],
            {self.header: None}
        ]
        result = _change_header_display_name(responses, self.header,
                                             self.custom_header)
        self.assertEqual(result, expected_responses)

    def test_change_header_display_name_dict(self):
        single_response = {
            self.header: 'data'
        }
        expected_single_response = {
            self.custom_header: 'data'
        }
        result = _change_header_display_name(single_response, self.header,
                                             self.custom_header)
        self.assertEqual(result, expected_single_response)


class TestCamelToTitle(unittest.TestCase):
    def test_camel_to_title(self):
        self.assertEqual(_camel_to_title('helloWorld'), 'Hello World')
        self.assertEqual(_camel_to_title('Hello_world'), 'Hello_World')
        self.assertEqual(_camel_to_title('hello'), 'Hello')
        self.assertEqual(_camel_to_title('Hello world'), 'Hello World')


class TestResolveDisableNumparseIndices(unittest.TestCase):
    def test_resolve_disable_numparse_indices(self):
        response_table_headers = ['header1', 'header2', 'header3',
                                  'header4', 'header5']
        headers_config = {
            'header1': {'disable_numparse': True},
            'header3': {'disable_numparse': True},
            'header5': {'disable_numparse': True}
        }
        expected_result = [0, 2, 4]
        result = _resolve_disable_numparse_indices(response_table_headers,
                                                   headers_config)
        self.assertEqual(result, expected_result)


class TestResolveHeaderDisplayName(unittest.TestCase):
    def test_resolve_header_display_name(self):
        self.header, self.custom_header = 'header_to_change', 'replacement'
        response = [
            [
                {self.header: 'data'}
            ]
        ]
        expected_response = [
            [
                {self.custom_header: 'data'}
            ]
        ]
        response_table_headers = [self.header, 'header2']
        expected_response_table_headers = [self.custom_header, 'header2']
        headers_config = {
            self.header: {
                HEADER_DISPLAY_NAME: self.custom_header
            },
            'header2': {}
        }
        result = _resolve_header_display_name(response, response_table_headers,
                                              headers_config)
        self.assertEqual(result[0], [])
        self.assertEqual(result[1], expected_response)
        self.assertEqual(response_table_headers,
                         expected_response_table_headers)


class TestTableDataContainer(unittest.TestCase):
    def setUp(self) -> None:
        self.headers = {
            'header1',
            'header2',
            'header3'
        }
        self.container = TableDataContainer(self.headers)

    def test_init(self):
        expected_items = {
            'header1': [],
            'header2': [],
            'header3': []
        }
        self.assertEqual(self.container.items, expected_items)

    def test_aggregate_initial_data(self):
        expected_items = {
            'header1': [],
            'header2': [],
            'header3': []
        }
        result = TableDataContainer. \
            _TableDataContainer__aggregate_initial_data(self.headers)
        self.assertEqual(result, expected_items)

    def test_add_value(self):
        expected_items = {
            'header1': ['value'],
            'header2': [],
            'header3': []
        }
        self.container._TableDataContainer__add_value('header1', 'value')
        self.assertEqual(self.container.items, expected_items)

    def test_aggregate_values(self):
        response_item = {
            'header1': 'value1',
            'header2': 'a' * 71,
        }
        expected_items = {
            'header1': ['value1', ],
            'header2': [f'{"a" * 70}{os.linesep}a', ],
            'header3': [None]
        }
        self.container.aggregate_values(response_item)
        self.assertEqual(self.container.items, expected_items)

    def test_item_value(self):
        for item_value in ({'is_str': False}, 'A string less than 70 chars'):
            result = TableDataContainer._TableDataContainer__item_value(
                item_value)
            self.assertEqual(result, item_value)

        item_value = ('a' * 70) + ('b' * 70) + 'I should be on the third line'
        result = TableDataContainer._TableDataContainer__item_value(item_value)
        self.assertEqual(result,
                         f'{"a" * 70}{os.linesep}'
                         f'{"b" * 70}{os.linesep}'
                         f'I should be on the third line')

    def test_get_table_data(self):
        result = self.container.get_table_data()
        self.assertTrue(len(result[0]) == 0)  # dict_keys
        self.assertEqual(list(result[1]), [])

        self.container.items['header1'] = ['value1', 'value2']
        self.container.items['header2'] = ['value3', 'value4', 'value5']
        self.container.items['header3'] = []
        result = self.container.get_table_data()
        self.assertEqual(list(result[0]), ['header1', 'header2'])
        self.assertEqual(result[1], [
            ['value1', 'value3'],
            ['value2', 'value4']
        ])


class TestTableView(unittest.TestCase):
    def setUp(self) -> None:
        self.table = 'table'
        self.display_name = 'display_name'

    def test_get_view_not_display_name(self):
        table_view = TableView(self.table, None)
        result = table_view.get_view()
        self.assertEqual(result, self.table)

    def test_get_view_success(self):
        table_view = TableView(self.table, self.display_name)
        expected_result = """display_name\ntable"""
        result = table_view.get_view()
        self.assertEqual(result, expected_result)


class TestResponseProcessorServiceProcessResponse(TestResponseProcessorService):
    def setUp(self) -> None:
        super().setUp()
        self.init_service_object()

    def test_process_response_error_not_fail_safe(self):
        message = 'error'
        response = {ERROR_FILED: message}
        with self.assertRaises(AssertionError) as context:
            self.service.process_response(response, fail_safe=False)
        self.assertEqual(str(context.exception), message)

    def test_process_response_error_fail_safe(self):
        message = 'error'
        response = {ERROR_FILED: message}
        expected_result = '{"error": "%s"}' % message
        result = self.service.process_response(response, fail_safe=True)
        self.assertEqual(result, expected_result)

    def test_process_response_output_configuration_none(self):
        self.cmd_def = {
            'output_configuration': {'none': True}
        }
        self.init_service_object()
        result = self.service.process_response({}, fail_safe=False)
        self.assertEqual(result, 'The command has been executed successfully')

    def test_process_response_success(self):
        data = 'data'
        response = {DATA_FIELD: data}
        result = self.service.process_response(response, False)
        self.assertEqual(result, data)


class TestResponseProcessorServiceCheckErrors(TestResponseProcessorService):
    def test_check_errors_readable_error_field_invalid_json(self):
        invalid_json = '{\'message\': "error"}'
        response = {READABLE_ERROR_FILED: invalid_json}
        with self.assertRaises(AssertionError) as context:
            self.service.check_errors(response)
        self.assertEqual(str(context.exception), invalid_json)

    def test_check_errors_readable_error_field_valid_json(self):
        response = {READABLE_ERROR_FILED: '{"message": "error"}'}
        with self.assertRaises(AssertionError) as context:
            self.service.check_errors(response)
        self.assertEqual(str(context.exception), 'error')

    def test_check_errors_error_field(self):
        message = 'error'
        response = {ERROR_FILED: message}
        with self.assertRaises(AssertionError) as context:
            self.service.check_errors(response)
        self.assertEqual(str(context.exception), message)

    def test_check_errors_status_failed(self):
        response = {STATUS: 'FAILED'}
        with self.assertRaises(AssertionError) as context:
            self.service.check_errors(response)
        self.assertEqual(str(context.exception),
                         'The service has failed to handle the request')


class TestResponseProcessorServicePrettifyResponse(TestResponseProcessorService):
    def setUp(self) -> None:
        super().setUp()
        self.nullable = True
        self.custom_full_view = False
        self.cmd_def = {
            'output_configuration': {
                'nullable': self.nullable
            }
        }

    def test_prettify_response_not_view_printer(self):
        self.view = 'not_available'
        self.init_service_object()
        with self.assertRaises(AssertionError) as context:
            self.service.prettify_response({})
        self.assertEqual(str(context.exception),
                         f'The view type {self.view} is not currently '
                         f'supported')

    def test_prettify_response_success(self):
        expected_result = 'result'
        view_printer_mock = MagicMock(return_value=expected_result)
        with patch('m3cli.services.response_processor_service.ResponseProcess'
                   'orService._ResponseProcessorService__full_view',
                   view_printer_mock):
            self.view = FULL_VIEW
            self.init_service_object()
            result = self.service.prettify_response({})
        self.assertEqual(result, expected_result)
        view_printer_mock.assert_called_with(
            [], self.detailed, self.nullable, self.custom_full_view,
        )


class TestResponseProcessorServiceFormatResponse(TestResponseProcessorService):
    def test_format_response(self):
        response = [
            {'key': 'value'},
            [{'key': 'value'}],
            'string',
            1,
            '{"is_json": true}',
        ]
        expected_response = [
            {'key': 'value'},
            [{'key': 'value'}],
            'string',
            '1',
            {"is_json": True},
        ]
        result = self.service.format_response(response)
        self.assertEqual(result, expected_response)


class TestResponseProcessorServiceFullView(TestResponseProcessorService):
    def test_full_view(self):
        responses = {
            'key1': 'value1',
            'key2': ['value2', 'value3'],
            'key3': {'key4': 'value4'}
        }
        self.init_service_object()
        result = self.service._ResponseProcessorService__full_view(responses)
        self.assertEqual(result,
                         '\n\nkey1 = value1\nkey2:\n- value2\n- '
                         'value3\nkey3:\n  key4 = value4\n')


class TestResponseProcessorServiceComposeTable(TestResponseProcessorService):
    def test_compose_table(self):
        tables = [TableView('table1', 'display_name1'),
                  TableView('table2', 'display_name2')]
        self.init_service_object()
        result = self.service._ResponseProcessorService__compose_table(tables)
        self.assertEqual(result,
                         'display_name1\ntable1\n\ndisplay_name2\ntable2')


class TestResponseProcessorServiceRemoveNone(TestResponseProcessorService):
    def setUp(self) -> None:
        super().setUp()
        self.fancy_object = [
            {None, 0, 'data'},
            [
                {
                    'key1': None,
                    'key2': 0,
                    'key3': '',
                    'key4': 'data',
                    None: 'data'
                }
            ],
            ('data', []),
            None
        ]
        self.init_service_object()

    def test_remove_none_retain_zeros(self):
        expected_result = [
            {0, 'data'},
            [
                {
                    'key2': 0,
                    'key4': 'data'
                }
            ],
            ('data', [])
        ]
        result = self.service._ResponseProcessorService__remove_none(
            self.fancy_object, retain_zeros=True)
        self.assertEqual(result, expected_result)

    def test_remove_none_not_retain_zeros(self):
        expected_result = [
            {0, 'data'},
            [{'key4': 'data'}],
            ('data', [])
        ]
        result = self.service._ResponseProcessorService__remove_none(
            self.fancy_object, retain_zeros=False)
        self.assertEqual(result, expected_result)


class TestResponseProcessorServiceUnmapResponse(TestResponseProcessorService):
    def setUp(self) -> None:
        super().setUp()
        self.unmap_key = 'unmap_key'
        self.cmd_def = {'output_configuration': {'unmap_key': self.unmap_key}}
        self.response = [{self.unmap_key: 'one'}, {self.unmap_key: 'two'},
                         {'key': 'value'}]
        self.init_service_object()

    def test_unmap_response_no_unmap_key(self):
        self.cmd_def = {}
        self.init_service_object()
        result = self.service._ResponseProcessorService__unmap_response(
            self.response)
        self.assertEqual(result, self.response)

    def test_unmap_response_success(self):
        expected_result = ['one', 'two']
        result = self.service._ResponseProcessorService__unmap_response(
            self.response)
        self.assertEqual(result, expected_result)
