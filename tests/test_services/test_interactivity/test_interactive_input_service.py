import os
from unittest.mock import patch, MagicMock, call

from m3cli.models.interactive_parameter import InteractiveParameter
from m3cli.services.request_service import BaseRequest
from tests.test_services.test_interactivity import TestInteractiveInputService


class TestInteractiveInputServiceCollectUserInput(TestInteractiveInputService):
    def test_collect_user_input(self):
        self.init_service_object()
        parameters = [InteractiveParameter({'name': 'param1',
                                            'type': 'STRING'}),
                      InteractiveParameter({'name': 'param2',
                                            'type': 'STRING'})]
        request = BaseRequest(command='command',
                              parameters={'interactive-mode': True})
        ask_parameter_value_mock = MagicMock()
        with patch('m3cli.services.interactivity.interactive_input_service.'
                   'InteractiveInputService._ask_parameter_values',
                   ask_parameter_value_mock):
            result = self.service.collect_user_input(parameters, request)
        self.assertEqual(result, parameters)
        ask_parameter_value_mock.assert_called_with(
            parameters=parameters,
            force_interactive_mode=True)


class TestInteractiveInputServiceApproveParameters(
        TestInteractiveInputService):
    def setUp(self) -> None:
        super().setUp()
        self.click_confirm_mock = MagicMock()
        self.click_echo_mock = MagicMock()
        self.click_confirm_patch = patch('m3cli.services.interactivity.'
                                         'interactive_input_service.click.'
                                         'confirm', self.click_confirm_mock)
        self.click_echo_patch = patch('m3cli.services.interactivity.'
                                      'interactive_input_service.click.'
                                      'echo', self.click_echo_mock)
        self.click_confirm_patch.start()
        self.click_echo_patch.start()

    def tearDown(self) -> None:
        self.click_echo_patch.stop()
        self.click_confirm_patch.stop()

    def test_approve_parameters(self):
        self.click_confirm_mock.return_value = True
        name1, name2 = 'param1', 'param2'
        parameters = [InteractiveParameter({'sensitive': True,
                                            'name': name1}),
                      InteractiveParameter({'value': 'param_value',
                                            'name': name2})]
        result = self.service.approve_parameters(parameters)
        self.assertTrue(result)
        self.click_echo_mock.assert_has_calls(
            [call(f'{os.linesep}Please review the parameters:{os.linesep}'),
             call(f'{name1}: (sensitive)'),
             call(f'{name2}: "param_value"')])
        self.click_confirm_mock.assert_has_calls([
            call(f'{os.linesep}Approve parameters')
        ])


class TestInteractiveInputServiceSelectParametersToAsk(
        TestInteractiveInputService):
    def test_select_parameters_to_ask(self):
        param1 = InteractiveParameter({'type': 'STRING'})
        param2 = InteractiveParameter({'type': 'LIST'})
        param3 = InteractiveParameter({'type': 'STRING'})
        parameters = [param1, param2, param3]
        result = self.service._select_parameters_to_ask(parameters)
        self.assertEqual(result, [param1, param2])


class TestInteractiveInputServiceAskParameterValue(
        TestInteractiveInputService):
    def setUp(self) -> None:
        super().setUp()
        self.param_without_value = InteractiveParameter({'name': 'param1',
                                                         'sensitive': True})
        self.param_force_prompt = InteractiveParameter({'name': 'param2'})
        self.param_force_prompt.force_prompt()

        self.value1, self.value2, self.value3 = 'first', 'second', 'three'
        self.param3_default_value = 'value3'
        self.param_with_value = InteractiveParameter({'name': 'param3'})
        self.param_with_value.value = self.param3_default_value

        self.parameters = [self.param_without_value, self.param_force_prompt,
                           self.param_with_value]
        self.click_prompt_mock = MagicMock()
        self.click_prompt_patch = patch('m3cli.services.interactivity.'
                                        'interactive_input_service.click.'
                                        'prompt', self.click_prompt_mock)
        self.click_prompt_patch.start()

    def tearDown(self) -> None:
        self.click_prompt_patch.stop()

    def test_ask_parameter_values_not_force(self):
        self.click_prompt_mock.side_effect = [self.value1, self.value2]
        result = self.service._ask_parameter_values(self.parameters, False)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].value, self.value1)
        self.assertEqual(result[1].value, self.value2)
        self.assertEqual(result[2].value, self.param3_default_value)
        self.click_prompt_mock.assert_has_calls([
            call(text='param1 (sensitive)', hide_input=True, default=None,
                 show_default=False),
            call(text='param2', hide_input=False, default=None,
                 show_default=True)
        ])

    def test_ask_parameter_values_force(self):
        self.click_prompt_mock.side_effect = [self.value1, self.value2,
                                              self.value3]
        result = self.service._ask_parameter_values(self.parameters, True)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].value, self.value1)
        self.assertEqual(result[1].value, self.value2)
        self.assertEqual(result[2].value, self.value3)
        self.click_prompt_mock.assert_has_calls([
            call(text='param1 (sensitive)', hide_input=True, default=None,
                 show_default=False),
            call(text='param2', hide_input=False, default=None,
                 show_default=True),
            call(text='param3', hide_input=False, default='value3',
                 show_default=True)
        ])
