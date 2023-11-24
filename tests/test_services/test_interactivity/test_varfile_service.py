import json
import os
import tempfile

import click

from m3cli.models.interactive_parameter import InteractiveParameter
from m3cli.services.interactivity.varfile.varfile_service import \
    VARFILE_PARAMETER, VARFILE_FORMAT_PARAMETER, JSON_FORMAT, HCL_FORMAT
from m3cli.services.interactivity.varfile.varfile_service import \
    VarfileHclAdapter, VarfileJsonAdapter
from m3cli.services.request_service import BaseRequest
from tests.test_services.test_interactivity import TestVarfileService


class TestVarfileServiceGenerateVarfileTemplate(TestVarfileService):
    def setUp(self) -> None:
        super().setUp()
        self.request = BaseRequest(command='command')
        self.parameters = [InteractiveParameter({'name': 'name1',
                                                 'value': 'value1'}),
                           InteractiveParameter({'name': 'name2',
                                                 'value': 'value2'})]
        self._varfile_parameter = tempfile.NamedTemporaryFile(delete=False)
        self._varfile_parameter.close()
        self.varfile_parameter = self._varfile_parameter.name

    def tearDown(self) -> None:
        if os.path.exists(self.varfile_parameter):
            os.remove(self.varfile_parameter)

    def test_generate_varfile_template_no_parameters(self):
        result = self.service.generate_varfile_template(self.request, [])
        self.assertIsNone(result)

    def test_generate_varfile_template(self):
        self.request.parameters = {
            VARFILE_PARAMETER: self.varfile_parameter,
            VARFILE_FORMAT_PARAMETER: JSON_FORMAT
        }
        result = self.service.generate_varfile_template(self.request,
                                                        self.parameters)
        self.assertIsNone(result)
        with open(self.varfile_parameter, 'r') as file:
            self.assertEqual(file.read(),
                             '{\n  "name1": "value1",\n  "name2": "value2"\n}')


class TestVarfileServiceReadVarfile(TestVarfileService):
    def setUp(self) -> None:
        super().setUp()
        self._varfile_parameter = tempfile.NamedTemporaryFile(delete=False)
        self._varfile_parameter.close()
        self.varfile_parameter = self._varfile_parameter.name
        self.request_params = {
            VARFILE_PARAMETER: self.varfile_parameter,
            VARFILE_FORMAT_PARAMETER: JSON_FORMAT
        }

    def tearDown(self) -> None:
        if os.path.exists(self.varfile_parameter):
            os.remove(self.varfile_parameter)

    def test_read_varfile_empty_file(self):
        result = self.service.read_varfile(self.request_params)
        self.assertEqual(result, {})

    def test_read_varfile_invalid_json(self):
        invalid_json = '{\'key": "value"}'
        with open(self.varfile_parameter, 'w') as file:
            file.write(invalid_json)
        with self.assertRaises(click.exceptions.Exit):
            self.service.read_varfile(self.request_params)

    def test_read_varfile_success(self):
        data = {'key': 'data'}
        with open(self.varfile_parameter, 'w') as file:
            json.dump(data, file)
        result = self.service.read_varfile(self.request_params)
        self.assertEqual(result, data)


class TestVarfileServiceIsVarfileInvalid(TestVarfileService):
    def setUp(self) -> None:
        super().setUp()
        self.parameters = [InteractiveParameter({'type': 'STRING'}),
                           InteractiveParameter({'type': 'STRING'})]

    def test_is_param_invalid_true(self):
        self.parameters.append(InteractiveParameter({'type': 'NOT STRING'}))
        self.assertTrue(self.service.is_varfile_invalid(self.parameters))

    def test_is_param_invalid_false(self):
        self.assertFalse(self.service.is_varfile_invalid(self.parameters))


class TestVarfileServiceResolveParameterValue(TestVarfileService):
    def setUp(self) -> None:
        super().setUp()
        self.value, self.type = 'value', 'map'
        self.parameter = InteractiveParameter({'type': self.type})

    def test_resolve_parameter_value_exists(self):
        self.parameter.value = self.value
        result = self.service._resolve_parameter_value(self.parameter)
        self.assertEqual(result, self.value)

    def test_resolve_parameter_value_does_not_exist(self):
        result = self.service._resolve_parameter_value(self.parameter)
        self.assertEqual(result, {})


class TestVarfileServiceSaveVarfile(TestVarfileService):
    def setUp(self) -> None:
        super().setUp()
        self._varfile_parameter = tempfile.NamedTemporaryFile(delete=False)
        self._varfile_parameter.close()
        self.varfile_parameter = self._varfile_parameter.name

    def tearDown(self) -> None:
        if os.path.exists(self.varfile_parameter):
            os.remove(self.varfile_parameter)

    def test_save_varfile(self):
        model = {'key': 'value'}
        result = self.service._save_varfile(
            model, {VARFILE_PARAMETER: self.varfile_parameter,
                    VARFILE_FORMAT_PARAMETER: JSON_FORMAT})
        self.assertEqual(result, self.varfile_parameter)
        with open(self.varfile_parameter, 'r') as file:
            self.assertEqual(file.read(), '{\n  "key": "value"\n}')


class TestVarfileServiceResolveVarfilePath(TestVarfileService):
    def setUp(self) -> None:
        super().setUp()
        self.service_name = 'service_name'
        self.actual_dir = os.getcwd()
        self.tempdir = tempfile.gettempdir()
        os.chdir(self.tempdir)

    def tearDown(self) -> None:
        os.chdir(self.actual_dir)

    def test_resolve_varfile_path_in_request_parameters(self):
        path = 'path'
        result = self.service._resolve_varfile_path({VARFILE_PARAMETER: path})
        self.assertEqual(result, path)

    def test_resolve_varfile_path_json(self):
        result = self.service._resolve_varfile_path({
            'serviceName': self.service_name,
            VARFILE_FORMAT_PARAMETER: JSON_FORMAT
        })
        self.assertEqual(result, os.path.join(
            self.tempdir, f'{self.service_name}.varfile.tfvars.json'))

    def test_resolve_varfile_path_hcl(self):
        result = self.service._resolve_varfile_path({
            'serviceName': self.service_name,
            VARFILE_FORMAT_PARAMETER: HCL_FORMAT
        })
        self.assertEqual(result, os.path.join(
            self.tempdir, f'{self.service_name}.varfile.tfvars'))


class TestVarfileServiceGetIOAdapter(TestVarfileService):
    def test_get_io_adapter_not_supported(self):
        format = 'not_supported_format'
        with self.assertRaises(ValueError) as context:
            self.service._get_io_adapter({VARFILE_FORMAT_PARAMETER: format})
        self.assertEqual(str(context.exception), f'{format} variables file '
                                                 f'format is not supported')

    def test_get_io_adapter_success_json(self):
        result = self.service._get_io_adapter({
            VARFILE_FORMAT_PARAMETER: JSON_FORMAT
        })
        self.assertIsInstance(result, VarfileJsonAdapter)

    def test_get_io_adapter_success_hcl(self):
        result = self.service._get_io_adapter({
            VARFILE_FORMAT_PARAMETER: HCL_FORMAT
        })
        self.assertIsInstance(result, VarfileHclAdapter)
