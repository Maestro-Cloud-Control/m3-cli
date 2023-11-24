from unittest.mock import MagicMock, patch

from m3cli.models.interactive_parameter import InteractiveParameter
from tests.test_services.test_interactivity import TestParametersProvider


class TestParametersProviderFetchInteractiveParameters(TestParametersProvider):
    def setUp(self) -> None:
        super().setUp()
        self.request_parameters = {'key': 'value'}
        self.sdk_client_mock = MagicMock()
        self.sdk_client_patch = patch('m3cli.services.interactivity.'
                                      'parameters_provider.SdkClient',
                                      self.sdk_client_mock)
        self.sdk_client_patch.start()

    def tearDown(self) -> None:
        self.sdk_client_patch.stop()

    def test_fetch_interactive_parameters_not_response_data_readable(self):
        readable = 'readable_error'
        self.sdk_client_mock().execute.return_value = \
            ({}, [{'readableError': readable}])
        with self.assertRaises(AssertionError) as context:
            self.service.fetch_interactive_parameters(self.request_parameters)
        self.assertEqual(str(context.exception),
                         'An error has occurred while processing the request. '
                         f'{readable}')

    def test_fetch_interactive_parameters_not_response_data(self):
        error = 'error'
        self.sdk_client_mock().execute.return_value = \
            ({}, [{'error': error}])
        with self.assertRaises(AssertionError) as context:
            self.service.fetch_interactive_parameters(self.request_parameters)
        self.assertEqual(str(context.exception),
                         'An error has occurred while processing the request. '
                         f'{error}')

    def test_fetch_interactive_parameters_success(self):
        self.sdk_client_mock().execute.return_value = \
            ({}, [{'data': '[{"name": "param1"}, {"name": "param2"}]'}])
        result = self.service.fetch_interactive_parameters(
            self.request_parameters)
        for param in result:
            self.assertIsInstance(param, InteractiveParameter)
        self.assertEqual(result[0].name, 'param1')
        self.assertEqual(result[1].name, 'param2')

        execute_kwargs = self.sdk_client_mock().execute.mock_calls[0].kwargs
        self.assertIn('request', execute_kwargs)
        request = execute_kwargs['request']
        self.assertEqual(request.command, 'get_parameters')
        self.assertEqual(request.api_action, self.api_action)
        self.assertEqual(request.parameters, self.request_parameters)
        self.assertEqual(request.method, 'POST')
