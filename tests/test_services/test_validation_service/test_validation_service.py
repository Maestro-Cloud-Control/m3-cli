import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

from m3cli.services.validation_service import VALIDATION_REGEX, \
    VALIDATION_ALLOWED_VALUES, COMMANDS_KEY, GROUPS_KEY, PARAMS_KEY, \
    DOMAIN_PARAMETERS_KEY, LIST_SEPARATOR, DATE_PATTERN, ROOT_DEFAULT, \
    VALIDATION_ALLOWED_FILE_EXTENSIONS, SUPPORTED_IMAGE_TYPES, \
    VALIDATION_REGEX_ERROR, VALIDATION_MAX_FILE_SIZE
from tests.test_services.test_validation_service import \
    TestValidationService, TestValidationServiceCheck


class TestValidationServiceValidateMeta(TestValidationService):
    def setUp(self) -> None:
        super().setUp()
        self.command_name = 'command_name'
        self.param_name = 'param_name'
        self.param_def = {
            'help': 'param help string',
            'validation': {
                'type': 'bool'
            }
        }
        self.domain_param_name = 'domain_param_name'
        self.domain_param_def = {
            'help': 'domain param help string',
            'validation': {
                'type': 'number'
            }
        }
        self.commands_def = {
            GROUPS_KEY: ['first', 'second'],
            COMMANDS_KEY: {
                self.command_name: {
                    'output_configuration': {
                        'response_table_headers': []
                    },
                    GROUPS_KEY: [
                        'cli-auxiliary_group-help',
                        'email-test-group'
                    ],
                    PARAMS_KEY: {
                        self.param_name: self.param_def,
                    },
                }
            },
            DOMAIN_PARAMETERS_KEY: {
                self.domain_param_name: self.domain_param_def,
            }
        }

    def test_validate_meta_not_commands(self):
        self.commands_def.update({COMMANDS_KEY: {}})
        result = self.service.validate_meta(self.commands_def)
        self.assertEqual(result[0], 'File with commands configuration must '
                                    'contain \'commands\' attribute')

    def test_validate_meta_not_defined_group(self):
        group = 'third'
        self.commands_def[COMMANDS_KEY][self.command_name][GROUPS_KEY]. \
            append(group)
        result = self.service.validate_meta(self.commands_def)
        self.assertEqual(result[0],
                         f'Command \'{self.command_name}\': \'{group}\' '
                         f'command group is not defined')

    def test_validate_meta_wrong_schema(self):
        # one case
        self.commands_def[COMMANDS_KEY][self.command_name].get(
            'output_configuration').pop('response_table_headers')
        result = self.service.validate_meta(self.commands_def)
        self.assertEqual(result[0],
                         f'Command \'{self.command_name}\': '
                         '\'response_table_headers\' is a required property')

        # another case
        self.commands_def[COMMANDS_KEY][self.command_name]. \
            pop('output_configuration')
        result = self.service.validate_meta(self.commands_def)
        self.assertEqual(result[0],
                         f'Command \'{self.command_name}\': '
                         '\'output_configuration\' is a required property')

    def test_validate_meta_not_defined_group_and_wrong_schema(self):
        """Multiple errors"""
        self.commands_def[COMMANDS_KEY][self.command_name].get(
            'output_configuration').pop('response_table_headers')
        group = 'third'
        self.commands_def[COMMANDS_KEY][self.command_name][GROUPS_KEY]. \
            append(group)

        result = self.service.validate_meta(self.commands_def)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0],
                         f'Command \'{self.command_name}\': \'{group}\' '
                         f'command group is not defined')
        self.assertEqual(result[1],
                         f'Command \'{self.command_name}\': '
                         '\'response_table_headers\' is a required property')

    def test_validate_meta_wrong_params_schema(self):
        result = self.service.validate_meta(self.commands_def)
        self.assertEqual(result, [])

        self.param_def['validation'].pop('type')
        result = self.service.validate_meta(self.commands_def)
        self.assertEqual(result[0],
                         f'Command \'{self.command_name}\': parameter '
                         f'\'{self.param_name}\' - \'type\' is a required '
                         f'property')

        self.param_def.pop('help')
        result = self.service.validate_meta(self.commands_def)
        self.assertEqual(result[0],
                         f'Command \'{self.command_name}\': parameter '
                         f'\'{self.param_name}\' - \'help\' is a required '
                         f'property')

        self.param_def.pop('validation')
        result = self.service.validate_meta(self.commands_def)
        self.assertEqual(result[0],
                         f'Command \'{self.command_name}\': parameter '
                         f'\'{self.param_name}\' - \'validation\' is a '
                         f'required property')

    def test_validate_meta_domain_param_schema(self):
        self.param_def.clear()
        self.param_def.update({
            'parent': self.domain_param_name
        })
        result = self.service.validate_meta(self.commands_def)
        self.assertEqual(result, [])

        self.domain_param_def.pop('validation').pop('type')
        result = self.service.validate_meta(self.commands_def)
        self.assertEqual(result[0],
                         f'Command \'{self.command_name}\': parameter '
                         f'\'{self.param_name}\' - \'type\' is a required '
                         f'property')


class TestValidationServiceValidateValue(TestValidationServiceCheck):
    def setUp(self) -> None:
        super().setUp()
        self.value = 'value'
        self.type = 'custom_type'
        self.handler_result = 'result'
        self.type_handler = MagicMock(return_value=self.handler_result)
        self.validation_rules.update({
            'type': self.type
        })
        self.service.types_handler_mapping = {
            self.type: self.type_handler
        }

    def test_validate_value_not_param_value(self):
        with self.assertRaises(AssertionError) as context:
            self.service.validate_value(self.param_name, None, {})
        self.assertEqual(str(context.exception),
                         f'Expected a value after parameter {self.param_name}')

    def test_validate_value_not_type_specified(self):
        self.validation_rules['type'] = None
        with self.assertRaises(AssertionError) as context:
            self.service.validate_value(self.param_name, self.value,
                                        self.validation_rules)
        self.assertEqual(str(context.exception),
                         'Attribute \'type\' is mandatory in '
                         'parameter validation section')

    def test_validate_value_success(self):
        result = self.service.validate_value(self.param_name, self.value, {})
        self.assertIsNone(result)

        result = self.service.validate_value(self.param_name, self.value,
                                             self.validation_rules)
        self.assertEqual(result, self.handler_result)
        self.type_handler.assert_called_with(
            param_name=self.param_name,
            value=self.value,
            validation_rules=self.validation_rules
        )


class TestValidationServiceGetDefaultValueForParam(TestValidationServiceCheck):
    def setUp(self) -> None:
        super().setUp()
        self.default_value_type = 'default_value_test_type'
        self.default_value = MagicMock()
        self.validation_rules.update({
            'type': self.default_value_type
        })

    def test_get_default_value_for_param_not_validation_rules(self):
        result = self.service.get_default_value_for_param({})
        self.assertEqual(result, ROOT_DEFAULT)

    def test_get_default_value_for_param_specified(self):
        self.service.default_values_mapping = {
            self.default_value_type: self.default_value
        }
        result = self.service.get_default_value_for_param(
            self.validation_rules
        )
        self.assertEqual(result, self.default_value)

    def test_get_default_value_for_param_not_specified(self):
        result = self.service.get_default_value_for_param(
            self.validation_rules
        )
        self.assertEqual(result, ROOT_DEFAULT)


class TestValidationServiceAdaptActualValue(TestValidationServiceCheck):
    def setUp(self) -> None:
        super().setUp()
        self.param_value = 'param_value'
        self.type = 'adapter_test_type'
        self.adapter_result = 'adapter_result'
        self.type_rule = MagicMock(return_value=self.adapter_result)
        self.validation_rules.update({
            'type': self.type
        })

    def test_adapt_actual_value_not_validation_rules(self):
        result = self.service.adapt_actual_value(self.param_value, {})
        self.assertEqual(result, self.param_value)

    def test_adapt_actual_value_adapter_not_specified(self):
        result = self.service.adapt_actual_value(self.param_value,
                                                 self.validation_rules)
        self.assertEqual(result, self.param_value)

    def test_adapt_actual_value_adapter_specified(self):
        self.service.adapt_values_mapping = {
            self.type: self.type_rule
        }
        result = self.service.adapt_actual_value(self.param_value,
                                                 self.validation_rules)
        self.assertEqual(result, self.adapter_result)
        self.type_rule.assert_called_with(actual_value=self.param_value)


class TestValidationServiceCheckString(TestValidationServiceCheck):
    def setUp(self) -> None:
        super().setUp()
        self.regex = r'value_\d+'
        self.allowed_values = ['value_1', 'value_2']
        self.validation_rules.update({
            VALIDATION_REGEX: self.regex,
            VALIDATION_ALLOWED_VALUES: self.allowed_values
        })

    def test_check_string_not_str(self):
        value = True
        result = self.service.check_string(self.param_name, value, {})
        self.assertEqual(
            result[0], f"Type of parameter '{self.param_name}' is not str"
        )

    def test_check_string_regex_does_not_match(self):
        value = 'wrong_value1'
        result = self.service.check_string(self.param_name, value,
                                           self.validation_rules)
        self.assertEqual(result[0],
                         f'The value of {self.param_name} does not match the '
                         f'RegExp value "{self.regex}"')

    def test_check_string_not_in_allowed(self):
        value = 'value_3'
        result = self.service.check_string(self.param_name, value,
                                           self.validation_rules)
        self.assertEqual(result[0],
                         f'The value of {self.param_name} should be one of '
                         f'allowed values: {self.allowed_values}. '
                         f'Actual value: {value}')

    def test_check_string_success(self):
        value = 'value_1'
        result = self.service.check_string(self.param_name, value,
                                           self.validation_rules)
        self.assertIsNone(result)

        self.validation_rules.pop(VALIDATION_ALLOWED_VALUES)
        result = self.service.check_string(self.param_name, value,
                                           self.validation_rules)
        self.assertIsNone(result)


class TestValidationServiceCheckNumber(TestValidationServiceCheck):
    def setUp(self) -> None:
        super().setUp()
        self.min_value, self.max_value = 0, 10
        self.validation_rules.update({
            'min_value': self.min_value,
            'max_value': self.max_value
        })

    def test_check_number_not_a_number(self):
        value = 'not a number'
        result = self.service.check_number(self.param_name, value, {})

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], f'Type of {self.param_name} is not '
                                    f'number.')

    def test_check_number_less_than_necessary(self):
        value = -1
        result = self.service.check_number(self.param_name, value,
                                           self.validation_rules)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0],
                         f'The value of {self.param_name} should be greater '
                         f'or equal than {self.min_value}. Actual: {value}')

    def test_check_number_greater_than_necessary(self):
        value = 11
        result = self.service.check_number(self.param_name, value,
                                           self.validation_rules)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0],
                         f'The value of {self.param_name} should be '
                         f'less than {self.max_value}. Actual: {value}')

    def test_check_number_success(self):
        value = 5
        result = self.service.check_number(self.param_name, value,
                                           self.validation_rules)
        self.assertEqual(result, [])


class TestValidationServiceCheckList(TestValidationServiceCheck):
    def setUp(self) -> None:
        super().setUp()
        self.value = LIST_SEPARATOR.join(['first', 'second', 'third'])
        self.allowed_values = ['first', 'second', 'fourth']
        self.validation_rules.update({
            VALIDATION_ALLOWED_VALUES: self.allowed_values
        })

    def test_check_list_success(self):
        result = self.service.check_list(self.param_name, self.value, {})
        self.assertIsNone(result)

    def test_check_list_not_in_allowed(self):
        result = self.service.check_list(self.param_name, self.value,
                                         self.validation_rules)
        self.assertEqual(result[0],
                         f'Range of values for list {self.param_name} is '
                         f'limited by these values: '
                         f'{", ".join(self.allowed_values)}. '
                         f'The following values are unknown: '
                         f'{", ".join(["third"])}')


class TestValidationServiceCheckObject(TestValidationServiceCheck):
    def setUp(self) -> None:
        super().setUp()
        self.property = 'property_1'
        self.validation_rules.update({
            'properties': {
                self.property: {
                    'type': 'string'
                }
            },
            'required': [self.property, ]
        })

    def test_check_object_not_object(self):
        result = self.service.check_object(self.param_name,
                                           'key1:value1,key2value2',
                                           self.validation_rules)
        self.assertEqual(result[0],
                         f'Type of {self.param_name} is not object.')

    def test_check_object_wrong_schema(self):
        result = self.service.check_object(self.param_name,
                                           'uncertain_property:value',
                                           self.validation_rules)
        self.assertEqual(result[0],
                         'The param_name value does not corresponds to the '
                         f'schema; Reason: \'{self.property}\' is a required '
                         'property')

    def test_check_object_success(self):
        result = self.service.check_object(self.param_name,
                                           'key1:value1,key2:value2', {})
        self.assertIsNone(result)

        result = self.service.check_object(self.param_name,
                                           'property_1:value',
                                           self.validation_rules)
        self.assertIsNone(result)


class TestValidationServiceCheckDate(TestValidationServiceCheck):
    def test_check_date_success(self):
        value = '17.01.2022'
        result = self.service.check_date(self.param_name, value, {})
        self.assertIsNone(result)

    def test_check_date_invalid_format(self):
        value = '01/17/2022'
        result = self.service.check_date(self.param_name, value, {})
        self.assertEqual(result[0],
                         f'Expected date format for parameter '
                         f'{self.param_name}: {DATE_PATTERN}. '
                         f'Given value: {value}')


class TestValidationServiceCheckBool(TestValidationServiceCheck):
    def test_check_bool_success(self):
        result = self.service.check_bool(self.param_name, True, {})
        self.assertIsNone(result)
        result = self.service.check_bool(self.param_name, False, {})
        self.assertIsNone(result)
        result = self.service.check_bool(self.param_name, 'True', {})
        self.assertIsNone(result)
        result = self.service.check_bool(self.param_name, 'False', {})
        self.assertIsNone(result)
        result = self.service.check_bool(self.param_name, 'true', {})
        self.assertIsNone(result)
        result = self.service.check_bool(self.param_name, 'false', {})
        self.assertIsNone(result)

    def test_check_bool_not_boolean(self):
        """Method:
         `m3cli.services.validation_service.ValidationService.check_bool in
         version 3.55.3 concludes any given value to be boolean.
         Should be corrected.
         """


class TestValidationServiceCheckFile(TestValidationServiceCheck):
    def setUp(self) -> None:
        super().setUp()
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.value = self.temp_file.name

    def tearDown(self) -> None:
        if os.path.exists(self.value):
            os.remove(self.value)

    def test_check_file_does_not_exist(self):
        os.remove(self.value)
        result = self.service.check_file(self.param_name, self.value,
                                         self.validation_rules)
        self.assertEqual(result[0], f'The "{self.value}" file does not exist')

    def test_check_file_regex_does_not_match(self):
        regex = r'regex_[1-9]+'
        regex_error = 'wrong regex'
        self.validation_rules.update({
            VALIDATION_REGEX: regex
        })
        result = self.service.check_file(self.param_name, self.value,
                                         self.validation_rules)
        self.assertEqual(result[0],
                         f'The name of the file does not match the '
                         f'RegExp value "{regex}"')

        self.validation_rules.update({
            VALIDATION_REGEX: regex,
            VALIDATION_REGEX_ERROR: regex_error
        })
        result = self.service.check_file(self.param_name, self.value,
                                         self.validation_rules)
        self.assertEqual(result[0], regex_error)

    def test_check_file_exceeded_max_size(self):
        self.validation_rules.update({
            VALIDATION_MAX_FILE_SIZE: 3  # 3 bytes
        })
        with open(self.temp_file.name, 'w') as file:
            file.write('123456789')  # certainly more than 3 bytes

        result = self.service.check_file(self.param_name, self.value,
                                         self.validation_rules)
        self.assertIn('The file exceeds the maximum allowed size', result[0])

    def test_check_file_success(self):
        result = self.service.check_file(self.param_name, self.value,
                                         self.validation_rules)
        self.assertEqual(result, [])


class TestValidationServiceCheckFileType(TestValidationServiceCheck):
    def setUp(self) -> None:
        super().setUp()
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.png',
                                                     delete=False)
        self.temp_file.close()
        self.value = Path(self.temp_file.name)

        self.allowed_extensions = {'.zip', }
        self.validation_rules.update({
            VALIDATION_ALLOWED_FILE_EXTENSIONS: self.allowed_extensions
        })

    def tearDown(self) -> None:
        if os.path.exists(self.value):
            os.remove(self.value)

    def test_check_file_type_not_in_allowed(self):
        result = self.service.check_file_type(self.value,
                                              self.validation_rules)
        self.assertEqual(result[0],
                         f'The file must have one of these extensions — '
                         f'{", ".join(self.allowed_extensions)}')

    def test_check_file_type_corrupter(self):
        """Assuming that created by python temp-file cannot be a valid image"""
        self.allowed_extensions.clear()
        self.allowed_extensions.add('.png')
        result = self.service.check_file_type(self.value,
                                              self.validation_rules)
        types = (t[1:].upper()
                 for t in self.allowed_extensions & SUPPORTED_IMAGE_TYPES)
        self.assertEqual(result[0],
                         f'The "{self.value}" image is corrupted. Please, '
                         f'provide a valid image of one of these types: '
                         f'{", ".join(types)}')

    def test_check_file_type_success(self):
        self.allowed_extensions.clear()
        result = self.service.check_file_type(self.value,
                                              self.validation_rules)
        self.assertEqual(result, [])


class TestValidationServiceUtils(TestValidationService):
    """Tests for methods: standardize_extension, adapt_list, adapt_object,
    adapt_date"""

    def test_standardize_extension(self):
        result = self.service.standardize_extension('.jpg')
        self.assertEqual(result, '.jpeg')

        extension = 'png'
        result = self.service.standardize_extension(extension)
        self.assertEqual(result, extension)

    def test_adapt_list(self):
        actual_value = LIST_SEPARATOR.join(['first ', 'second\n', '  third '])
        expected_value = ['first', 'second', 'third']

        result = self.service.adapt_list(actual_value)
        self.assertEqual(result, expected_value)

    def test_adapt_object(self):
        actual_value = LIST_SEPARATOR.join(['key1:value1', 'key2:value2'])
        expected_value = {
            'key1': 'value1',
            'key2': 'value2'
        }
        result = self.service.adapt_object(actual_value)
        self.assertEqual(result, expected_value)

    def test_adapt_date(self):
        actual_value = '17.01.2022'
        result = self.service.adapt_date(actual_value)
        self.assertEqual(result, 1642377600000)
