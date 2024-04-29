from unittest.mock import MagicMock, patch, call

from m3cli.models.interactive_parameter import InteractiveParameter
from tests.test_services.test_interactivity import TestRemoteValidationService


class TestRemoteValidationServiceValidateParameters(
        TestRemoteValidationService):
    def setUp(self) -> None:
        super().setUp()
        self.init_service_object()
        self.request_remote_validation_mock = MagicMock()
        self.request_remote_validation_patch = patch(
            'm3cli.services.interactivity.remote_validation_service.'
            'RemoteValidationService._request_remote_validation',
            self.request_remote_validation_mock)
        self.request_remote_validation_patch.start()

    def tearDown(self) -> None:
        self.request_remote_validation_patch.stop()

    def test_validate_parameters(self):
        message1, message3 = 'message1', 'message3'
        validation_result = [
            {'errorMessage': message1, 'name': 'param1'},
            {'name': 'param2'},
            {'errorMessage': message3, 'name': 'param3'}
        ]
        self.request_remote_validation_mock.return_value = validation_result
        parameter1 = InteractiveParameter({'name': 'param1',
                                           'type': 'LIST'})
        parameter3 = InteractiveParameter({'name': 'param3',
                                           'type': 'LIST'})
        parameters = [parameter1, parameter3]
        result = self.service.validate_parameters(parameters, "TEST")
        self.request_remote_validation_mock.assert_has_calls(
            [call(api_action='API_ACTION',
                  parameters={
                      'dtoList': [
                          {'name': 'param1',
                           'value': None,
                           'defaultValue': None,
                           'type': 'LIST',
                           'sensitive': False
                           },
                          {'name': 'param3',
                           'value': None,
                           'defaultValue': None,
                           'type': 'LIST',
                           'sensitive': False
                           }
                      ],
                      'serviceName': 'TEST'
                  })
             ]
        )
        self.assertEqual(result, {
            parameter1: message1,
            parameter3: message3
        })


class TestRemoteValidationServiceRequestRemoveValidation(
        TestRemoteValidationService):
    def setUp(self) -> None:
        super().setUp()
        self.api_action = 'API_ACTION'
        self.parameters = {'key': 'value'}
        self.sdk_client_mock = MagicMock()
        self.sdk_client_patch = patch('m3cli.services.interactivity.'
                                      'remote_validation_service.SdkClient',
                                      self.sdk_client_mock)
        self.sdk_client_patch.start()

    def tearDown(self) -> None:
        self.sdk_client_patch.stop()

    def test_request_remote_validation_not_data(self):
        response_item = {'error': 'error message'}
        self.sdk_client_mock().execute.return_value = ({}, [response_item])
        with self.assertRaises(AssertionError) as context:
            self.service._request_remote_validation(self.api_action,
                                                    self.parameters)
        self.assertEqual(str(context.exception),
                         f'Failed to validate parameters while applying '
                         f'interactive mode. Reason: {response_item}. '
                         f'Please contact Maestro Support Team.')

    def test_request_remote_validation_success(self):
        response_item = {'data': '{"key": "value"}'}
        self.sdk_client_mock().execute.return_value = ({}, [response_item])
        result = self.service._request_remote_validation(self.api_action,
                                                         self.parameters)
        self.assertEqual(result, {'key': 'value'})

        execute_kwargs = self.sdk_client_mock().execute.mock_calls[0].kwargs
        self.assertIn('request', execute_kwargs)
        request = execute_kwargs['request']
        self.assertEqual(request.command, 'validate_parameters')
        self.assertEqual(request.api_action, self.api_action)
        self.assertEqual(request.parameters, self.parameters)
        self.assertEqual(request.method, 'POST')
