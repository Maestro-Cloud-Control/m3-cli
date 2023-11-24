import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

from m3cli.services.commands_service import CommandsService
from m3cli.services.commands_service import UPPER, LOWER, LIST, \
    M3_CLI_RESOURCES_DIR, COMMANDS_DEF_FILE_NAME, CASE_KEY, API_PARAM_NAME
from m3cli.services.commands_service import _resolve_commands_def_path
from m3cli.services.commands_service import _resolve_default_cr_path
from m3cli.services.commands_service import _resolve_parameter_case
from m3cli.services.commands_service import get_help_key
from m3cli.services.commands_service import load_parameters_from_json
from m3cli.services.interactive_options_service import \
    INTERACTIVE_OPTIONS_ATTRIBUTE
from m3cli.services.request_service import BaseRequest
from m3cli.services.validation_service import AUXILIARY_GROUP_PREFIX, \
    AUXILIARY_GROUP_SUFFIX, ROOT_DEFAULT
from m3cli.services.validation_service import HELP_KEY, ALIAS_KEY, \
    PARAMS_KEY, REQUIRED_KEY, COMMANDS_KEY, VALIDATION_KEY, VALIDATION_TYPE, \
    DATE_PATTERN, SECURE_KEY
from m3cli.utils import CREDENTIALS_FILE, CONFIGURATION_FOLDER_PATH
from m3cli.utils import M3_PROPERTIES_FILE
from tests.test_services.test_commands_service import TestCommandsService


class TestResolveParameterCase(unittest.TestCase):
    def test_resolve_parameter_case_upper_list(self):
        actual_value = ['first', 'SECOND', 'Third']
        expecter_result = ['FIRST', 'SECOND', "THIRD"]
        result = _resolve_parameter_case(UPPER, actual_value, LIST)
        self.assertEqual(result, expecter_result)

    def test_resolve_parameter_case_upper_single(self):
        actual_value = 'first'
        expecter_result = 'FIRST'
        result = _resolve_parameter_case(UPPER, actual_value, '')
        self.assertEqual(result, expecter_result)

    def test_resolve_parameter_case_lower_list(self):
        actual_value = ['FIRST', 'second', 'tHIRD']
        expecter_result = ['first', 'second', "third"]
        result = _resolve_parameter_case(LOWER, actual_value, LIST)
        self.assertEqual(result, expecter_result)

    def test_resolve_parameter_case_lower_single(self):
        actual_value = 'FIRST'
        expecter_result = 'first'
        result = _resolve_parameter_case(LOWER, actual_value, '')
        self.assertEqual(result, expecter_result)


class TestResolveCommandsDefPath(unittest.TestCase):
    def setUp(self) -> None:
        self._default_path_obj = tempfile.TemporaryDirectory()
        self.default_path = self._default_path_obj.name
        self._env_path_obj = tempfile.TemporaryDirectory()
        self.env_path = self._env_path_obj.name
        self.filename = 'test_commands_def.json'

    def tearDown(self) -> None:
        self._default_path_obj.cleanup()
        self._env_path_obj.cleanup()

    def test_resolve_commands_def_path_env_exists(self):
        expecter_result = str(Path(self.env_path, self.filename))
        result = str(Path(_resolve_commands_def_path(self.default_path,
                                                     self.env_path,
                                                     self.filename)))
        self.assertEqual(result, expecter_result)

    def test_resolve_commands_def_path_env_does_not_exist(self):
        expecter_result = str(Path(self.default_path, self.filename))
        result = str(Path(_resolve_commands_def_path(self.default_path,
                                                     None,
                                                     self.filename)))
        self.assertEqual(result, expecter_result)


class TestResolveDefaultCrPath(unittest.TestCase):
    def test_resolve_default_cr_path(self):
        filename = 'test_file'
        result = _resolve_default_cr_path(filename)
        self.assertEqual(result, str(Path(Path.home(), M3_CLI_RESOURCES_DIR,
                                          filename)))


class TestLoadParametersFromJson(unittest.TestCase):
    def setUp(self) -> None:
        self.file = tempfile.NamedTemporaryFile(delete=False)
        self.file.close()
        self.file_path = self.file.name

    def tearDown(self) -> None:
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_load_parameters_from_json_syntax_error(self):
        invalid_json = """
        {
            "invalid_json": ["one", 'two', 'three'],
        }
        """
        with open(self.file_path, 'w') as file:
            file.write(invalid_json)
        with self.assertRaises(SyntaxError) as context:
            load_parameters_from_json(self.file_path)
        self.assertEqual(str(context.exception),
                         f'{self.file_path} contains an invalid JSON')

    def test_load_parameters_from_json_success(self):
        reserved_keywords = ['reserved_key']
        valid_json = """
        {
            "key1": "value1",
            "key2": "value2",
            "reserved_key": "value3"
        }
        """
        expecter_result = {
            'key1': 'value1',
            'key2': 'value2'
        }
        with open(self.file_path, 'w') as file:
            file.write(valid_json)
        with patch('m3cli.services.commands_service.RESERVED_KEYWORDS',
                   reserved_keywords):
            result = load_parameters_from_json(self.file_path)
        self.assertEqual(result, expecter_result)


class TestGetHelpKey(unittest.TestCase):
    def setUp(self) -> None:
        self.help_string = 'help_string'
        self.cmd_def = {
            HELP_KEY: self.help_string
        }

    def test_get_help_key_absent(self):
        self.cmd_def.pop(HELP_KEY)
        result = get_help_key(self.cmd_def)
        self.assertEqual(result, ' ')

    def test_get_help_key_success(self):
        result = get_help_key(self.cmd_def)
        self.assertEqual(result, self.help_string)


class TestCommandsServiceInit(TestCommandsService):
    def test_init_commands_def_does_not_exist(self):
        self.init_service_object()
        os.remove(Path(self.m3cli_path, COMMANDS_DEF_FILE_NAME))

        with patch('m3cli.services.commands_service._resolve_default_cr_path',
                   return_value=self.default_cr_path) as default_cr_mock, \
                self.assertRaises(FileExistsError) as context:
            CommandsService(self.m3cli_path, self.validation_service)
        default_cr_mock.assert_called_with(file_name=CREDENTIALS_FILE)
        self.assertEqual(str(context.exception),
                         f'File with commands configuration is absent. '
                         f'Provided path: '
                         f'{str(Path(self.m3cli_path, COMMANDS_DEF_FILE_NAME))}'
                         f'\nPlease set environment variable '
                         f'{CONFIGURATION_FOLDER_PATH} to specify the folder '
                         f'containing m3cli configuration files.')


class TestCommandsServiceLoadCommandsDef(TestCommandsService):
    def test_load_commands_def_syntax_error(self):
        # invalid json
        self.COMMANDS_DEF = """{
            'groups': [],
            'domain_parameters': {},
            'commands': {},
            "version": "1"
        }"""
        with self.assertRaises(SyntaxError) as context:
            self.init_service_object()
        self.assertEqual(str(context.exception),
                         f'{COMMANDS_DEF_FILE_NAME} contains invalid JSON')

    def test_load_commands_def_success(self):
        self.COMMANDS_DEF = json.dumps({
            'groups': [],
            'domain_parameters': {},
            'commands': {
                'first': {'key1': 'value1'},
                'second': {'key2': 'value2'}
            },
            'version': '1'
        })
        expecter_result = {
            'groups': [],
            'domain_parameters': {},
            'commands': {
                'first': {'key1': 'value1', 'name': 'first'},
                'second': {'key2': 'value2', 'name': 'second'}
            },
            'version': '1'
        }
        self.init_service_object()
        self.assertEqual(self.service.commands_def, expecter_result)


class TestCommandsServiceGetHelpFromFile(TestCommandsService):
    def test_get_help_from_file_success(self):
        self.init_service_object()
        help_message = 'test help message'
        with patch('m3cli.commands_help.my_command', help_message,
                   create=True):
            result = self.service._CommandsService__get_help_from_file(
                'my-command')
        self.assertEqual(result, help_message)

    def test_get_help_from_file_not_found(self):
        self.init_service_object()
        result = self.service._CommandsService__get_help_from_file(
            'not-existing-test-command')
        self.assertIsNone(result)


class TestCommandsServiceValidateMeta(TestCommandsService):
    def test_validate_meta_success(self):
        validation_result = 'result'
        self.validation_service = MagicMock()
        self.validation_service.validate_meta.return_value = validation_result
        self.init_service_object()
        result = self.service.validate_meta()

        self.assertEqual(result, validation_result)
        self.validation_service.validate_meta.assert_called_with(
            meta=json.loads(self.COMMANDS_DEF)
        )


class TestCommandsServiceFindRelatedCommands(TestCommandsService):
    def test_find_related_commands_success(self):
        main_command_name = 'main_command'
        main_command_def = {
            "groups": [
                "group2",
            ]
        }
        commands_def = {
            "groups": [],
            "domain_parameters": {},
            "commands": {
                main_command_name: main_command_def,
                "command1": {
                    "groups": [
                        f"{AUXILIARY_GROUP_PREFIX}{main_command_name}"
                        f"{AUXILIARY_GROUP_SUFFIX}",
                    ]
                },
                "command2": {
                    "groups": [
                        "group2"
                    ]
                }
            },
            "version": "1"
        }
        expected_result_1 = {
            "groups": [
                f"{AUXILIARY_GROUP_PREFIX}{main_command_name}"
                f"{AUXILIARY_GROUP_SUFFIX}",
            ],
            "name": "command1"

        }
        expected_result_2 = {
            "groups": [
                "group2"
            ],
            "name": "command2"

        }
        self.COMMANDS_DEF = json.dumps(commands_def)
        self.init_service_object()
        result = self.service._find_related_commands(
            cmd_name=main_command_name, cmd_def=main_command_def
        )
        # self.assertEqual(result, sorted([expected_result_1, expected_result_2],
        #                                 key=lambda c: c['name']))
        self.assertIn(expected_result_1, result)
        self.assertIn(expected_result_2, result)


class TestCommandsServiceFormatCommandExample(TestCommandsService):
    def test_format_command_example(self):
        command = 'main_command'
        default_param, default_value = 'default_param', 'default_value'
        alias_param, alias = 'param_with_alias', 'p'
        self.DEFAULT_PARAMETERS = json.dumps({
            default_param: default_value
        })
        commands_def = {
            "groups": [],
            "domain_parameters": {},
            "commands": {
                command: {
                    PARAMS_KEY: {
                        alias_param: {
                            REQUIRED_KEY: True,
                            ALIAS_KEY: alias,
                            VALIDATION_KEY: {
                                VALIDATION_TYPE: "string"
                            }

                        },
                        default_param: {
                            REQUIRED_KEY: True,
                        },
                        "not_required_param": {
                            REQUIRED_KEY: False,
                        }
                    },
                    # 'name' automatically resolved in '__load_commands_def'
                    "name": command
                }
            },
            "version": "1"
        }
        expected_result = f'm3 {command} --{default_param} {default_value} ' \
                          f'-{alias} <{alias_param}>'
        self.init_service_object()
        result = self.service._format_command_example(
            commands_def[COMMANDS_KEY][command])
        self.assertEqual(result, expected_result)


class TestCommandsServiceFormatExampleParameter(TestCommandsService):
    def test_format_example_parameter_no_p_alias(self):
        result = self.service._format_example_parameter('name', 'value')
        self.assertEqual(result, '--name value')

    def test_format_example_parameter_with_p_alias(self):
        result = self.service._format_example_parameter('name', 'value', 'n')
        self.assertEqual(result, '-n value')


class TestCommandsServiceGetParameterPlaceholder(TestCommandsService):
    def test_get_parameter_placeholder_date(self):
        result = self.service._get_parameter_placeholder('name', 'date')
        self.assertEqual(result, f'<{DATE_PATTERN}>')

    def test_get_parameter_placeholder_list(self):
        actual_name, expected_result = 'test-param-list', 'test_param'
        result = self.service._get_parameter_placeholder(actual_name, LIST)
        self.assertEqual(result, f'<{expected_result}1>,<{expected_result}N>')

    def test_get_parameter_placeholder_another_type(self):
        result = self.service._get_parameter_placeholder('test-param', 'type')
        self.assertEqual(result, '<test_param>')


class TestCommandsServiceReplaceParametersAliases(TestCommandsService):
    def test_replace_parameters_aliases(self):
        incoming_parameters = {
            "-p1": "value1",
            "-p2": "value2",
            "-p3": "value3"
        }
        parameter_def = {
            "param1": {
                ALIAS_KEY: "p1"
            },
            "param2": {
                ALIAS_KEY: "p2"
            },
            "param3": {
            }
        }
        expected_result = {
            "param1": "value1",
            "param2": "value2",
            "-p3": "value3"
        }
        result = self.service._CommandsService__replace_parameters_aliases(
            incoming_parameters, parameter_def)
        self.assertEqual(result, expected_result)


class TestCommandsServiceResolveCommandDef(TestCommandsService):
    def setUp(self) -> None:
        super().setUp()
        self.command_name = 'command'
        self.command_alias = 'c'
        self.command_def = {
            HELP_KEY: "test command help",
            ALIAS_KEY: self.command_alias
        }
        self.COMMANDS_DEF = json.dumps({
            "groups": [],
            "domain_parameters": {},
            "commands": {
                self.command_name: self.command_def
            },
            "version": "1"
        })
        self.init_service_object()

    def test_resolve_command_def_exists(self):
        result = self.service._CommandsService__resolve_command_def(
            self.command_name)
        self.command_def.update({'name': self.command_name})
        self.assertEqual(result, (self.command_name, self.command_def))

    def test_resolve_command_def_alias_found(self):
        result = self.service._CommandsService__resolve_command_def(
            self.command_alias)
        self.command_def.update({'name': self.command_name})
        self.assertEqual(result, (self.command_name, self.command_def))

    def test_resolve_commands_def_not_found(self):
        name = 'not_existing'
        result = self.service._CommandsService__resolve_command_def(name)
        self.assertEqual(result, (name, None))


class TestCommandsServiceGetSecureParams(TestCommandsService):
    def test_get_secure_params_not_found(self):
        self.init_service_object()  # with defaults from TestCommandsService
        result = self.service.get_secure_params('not_existing')
        self.assertEqual(result, [])

    def test_get_secure_params_no_params(self):
        command_name = 'name'
        self.COMMANDS_DEF = json.dumps({
            "groups": [],
            "domain_parameters": {},
            "commands": {
                command_name: {
                    PARAMS_KEY: {}
                }
            },
            "version": "1"
        })
        self.init_service_object()
        result = self.service.get_secure_params(command_name)
        self.assertEqual(result, [])

    def test_get_secure_params_success(self):
        command_name = 'name'
        self.COMMANDS_DEF = json.dumps({
            "groups": [],
            "domain_parameters": {
                "param1": {
                    SECURE_KEY: True,
                    ALIAS_KEY: "p1"
                }
            },
            "commands": {
                command_name: {
                    PARAMS_KEY: {
                        "param1": {
                            "parent": "param1",
                        },
                        "param2": {
                            SECURE_KEY: True,
                            ALIAS_KEY: "p2"
                        },
                        "param3": {
                            SECURE_KEY: False
                        }
                    }
                }
            },
            "version": "1"
        })
        expected_result = ['-p1', 'param1', '-p2', 'param2']
        self.init_service_object()
        result = self.service.get_secure_params(command_name)
        self.assertEqual(result, expected_result)


class TestCommandsServiceValidateRequest(TestCommandsService):
    def setUp(self) -> None:
        super().setUp()
        self.command = 'command'
        self.api_action = 'ACTION'
        self.cmd_def = {
            "api_action": self.api_action,
            PARAMS_KEY: {
                'param1': {
                    ALIAS_KEY: 'p1',
                    REQUIRED_KEY: True,
                    VALIDATION_KEY: {
                        VALIDATION_TYPE: 'string'
                    }

                },
                'param2': {
                    ALIAS_KEY: 'p2',
                    REQUIRED_KEY: False,
                    VALIDATION_KEY: {
                        VALIDATION_TYPE: 'number'
                    }
                },
                'param3': {
                    ALIAS_KEY: 'p3',
                    VALIDATION_KEY: {
                        VALIDATION_TYPE: 'bool'
                    },
                    REQUIRED_KEY: False
                },
                'param4': {
                    VALIDATION_TYPE: {
                        VALIDATION_KEY: 'string'
                    }
                }

            }
        }
        self.COMMANDS_DEF = json.dumps({
            "groups": [],
            "domain_parameters": {},
            "commands": {
                self.command: self.cmd_def
            },
            "version": "1"
        })
        self.request = BaseRequest(command=self.command)
        self.init_service_object()

    def test_validate_request_unavailable_command(self):
        not_available_command = 'not_available'
        self.request.command = not_available_command
        result = self.service.validate_request(self.request)
        self.assertIsNone(result[0])
        self.assertEqual(result[1],
                         [f'Command \"{not_available_command}\" is invalid or '
                          f'is not available.\n'
                          f'Available commands: {[self.command]};'])

    def test_validate_request_missing_required(self):
        self.request.parameters = {
            '-p2': 55
        }
        result = self.service.validate_request(self.request)
        self.assertIsNone(result[0])
        self.assertEqual(result[1],
                         [f'The command {self.command} requires the following'
                          f' parameter: --param1 (-p1);'])

    def test_validate_request_unexpected_params(self):
        unexpected_param1, unexpected_param2 = 'param5', 'param6'
        self.request.parameters = {
            'param1': 'value1',
            unexpected_param1: 'value5',
            unexpected_param2: 'value6'
        }
        result = self.service.validate_request(self.request)
        self.assertIsNone(result[0])
        # It checks this way below because unexpected_params are resolved from
        # a set inside. There is no guarantee in which order it'll be returned
        self.assertTrue(result[1] == [f'The command command obtains '
                                      f'unexpected params: {unexpected_param2}'
                                      f', {unexpected_param1};']
                        or result[1] == [f'The command command obtains '
                                         f'unexpected params: '
                                         f'{unexpected_param1}, '
                                         f'{unexpected_param2};'])

    def test_validate_request_unexpected_value_after_the_flag_parameter(self):
        flag_param = 'param3'
        self.request.parameters = {
            'param1': 'value1',
            flag_param: 'value3'
        }
        result = self.service.validate_request(self.request)
        self.assertIsNone(result[0])
        self.assertEqual(result[1],
                         [f'Unexpected value after the flag '
                          f'parameter: {flag_param};'])

    def test_validate_request_validate_params(self):
        self.request.parameters = {
            'param1': 45,
            'param2': 'not_a_number'
        }
        result = self.service.validate_request(self.request)
        self.assertIsNone(result[0])
        self.assertEqual(result[1],
                         ['Type of param1 is not str.',
                          'Type of param2 is not number.'])

    def test_validate_request_success(self):
        self.request.parameters = {
            'param1': 'value1',
            'param2': 45,
        }
        expected_parameters = {
            'param1': 'value1',
            'param2': 45,
            'param4': ROOT_DEFAULT
        }
        result = self.service.validate_request(self.request)
        self.cmd_def.update({'name': self.command})
        self.assertEqual(result[0], self.cmd_def)
        self.assertEqual(result[1], [])
        self.assertEqual(self.request.parameters, expected_parameters)


class TestCommandsServiceGetCommandsDefVersion(TestCommandsService):
    def test_get_commands_def_version(self):
        self.init_service_object()
        result = self.service.get_commands_def_version()
        self.assertEqual(result, '1')  # '1' is from TestCommandsService


class TestCommandsServiceResolveParametersCase(TestCommandsService):
    def setUp(self) -> None:
        super().setUp()
        self.command = 'main_command'
        self.api_param_name = 'api_param_name'
        self.COMMANDS_DEF = json.dumps({
            "groups": [],
            "domain_parameters": {},
            "commands": {
                self.command: {
                    PARAMS_KEY: {
                        "param1": {
                            ALIAS_KEY: "p1",
                            CASE_KEY: UPPER,
                            VALIDATION_KEY: {
                                VALIDATION_TYPE: LIST
                            },
                            "no_api": True
                        },
                        "param2": {
                            ALIAS_KEY: "p2",
                            CASE_KEY: LOWER,
                            VALIDATION_KEY: {
                                VALIDATION_TYPE: "string"
                            },
                            'no_api': False,
                            API_PARAM_NAME: self.api_param_name
                        },
                        "param3": {

                        }
                    }
                }
            },
            "version": "1"
        })
        self.init_service_object()

    def test_resolve_parameters_case_not_cmd_def(self):
        command = 'not_existing'
        request = BaseRequest(command=command)
        result = self.service.resolve_parameters_case(request)
        self.assertIs(result, request)
        self.assertEqual(request.command, command)

    def test_resolve_parameters_case(self):
        parameters = {
            '-p1': ['first', 'second'],
            '-p2': 'THird'
        }
        expected_parameters = {
            'param1': ['FIRST', 'SECOND'],
            self.api_param_name: 'third'
        }
        request = BaseRequest(command=self.command, parameters=parameters)
        result = self.service.resolve_parameters_case(request)
        self.assertEqual(result.parameters, expected_parameters)


class TestCommandsServiceResolveParametersBatchProcessing(TestCommandsService):
    def setUp(self) -> None:
        super().setUp()
        self.param = 'param'
        self.api_param_name = 'api_param_name'
        self.cmd_def = {
            PARAMS_KEY: {
                self.param: {
                    VALIDATION_KEY: {
                        VALIDATION_TYPE: LIST
                    },
                    'batch_param': True,
                    API_PARAM_NAME: self.api_param_name
                }
            }
        }

    def test_resolve_parameters_batch_processing_not_list(self):
        self.cmd_def[PARAMS_KEY][self.param][VALIDATION_KEY][
            VALIDATION_TYPE] = 'string'
        with self.assertRaises(AssertionError) as context:
            self.service.resolve_parameters_batch_processing(
                self.cmd_def, BaseRequest('test_command'))
        self.assertEqual(str(context.exception),
                         'Only parameter with type \'list\' '
                         'can be used as batch parameter')

    def test_resolve_parameters_batch_processing_interactive_mode(self):
        self.cmd_def[INTERACTIVE_OPTIONS_ATTRIBUTE] = {
            'generate_varfile': True
        }
        with self.assertRaises(AssertionError) as context:
            self.service.resolve_parameters_batch_processing(
                self.cmd_def, BaseRequest('test_command')
            )
        self.assertEqual(str(context.exception),
                         'Batch requests are not allowed '
                         'for interactive mode')

    def test_resolve_parameters_batch_processing_no_batch_param(self):
        self.cmd_def[PARAMS_KEY][self.param][API_PARAM_NAME] = None
        request = BaseRequest('command')
        result = self.service.resolve_parameters_batch_processing(
            self.cmd_def, request
        )
        self.assertIs(result[0][0], request)
        self.assertTrue(result[1])

    def test_resolve_parameters_batch_processing_success(self):
        parameters = {
            self.api_param_name: ['value1', 'value2']
        }
        request = BaseRequest('command', parameters=parameters)
        result = self.service.resolve_parameters_batch_processing(
            self.cmd_def, request
        )
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[0][0], BaseRequest)
        self.assertIsInstance(result[0][1], BaseRequest)
        self.assertEqual(result[0][0].parameters, {
            self.api_param_name: 'value1'
        })
        self.assertEqual(result[0][1].parameters, {
            self.api_param_name: 'value2'
        })
        self.assertTrue(result[1])


class TestCommandsServiceLoadDefaultParameters(TestCommandsService):
    def setUp(self) -> None:
        super().setUp()
        self._m3_properties_folder = tempfile.TemporaryDirectory()
        self.m3_properties_folder = self._m3_properties_folder.name
        self.properties = """
        # comment
        key2=value2
        key3=value3
        """
        with open(Path(self.m3_properties_folder,
                       M3_PROPERTIES_FILE), 'w') as file:
            file.write(self.properties)
        self.init_service_object()

    def tearDown(self) -> None:
        self._m3_properties_folder.cleanup()
        super().tearDown()

    def test_load_default_parameters_m3_properties(self):
        expected_result = {
            'key1': 'value1',  # from TestCommandsService class variable
            'key2': 'value2',
            'key3': 'value3'
        }

        with patch('m3cli.services.commands_service.os.getcwd',
                   return_value=self.m3_properties_folder):
            result = self.service._load_default_parameters()
        self.assertEqual(result, expected_result)
