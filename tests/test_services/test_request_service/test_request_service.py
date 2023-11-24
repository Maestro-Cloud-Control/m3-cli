import json
import unittest
from unittest.mock import MagicMock, patch

import requests

from m3cli.services.request_service import BaseRequest
from m3cli.services.request_service import mask_params
from m3cli.services.request_service import verify_response
from m3cli.services.request_service import wrap_request
from tests.test_services.test_request_service import TestSdkClient


class TestWrapRequest(unittest.TestCase):
    def setUp(self) -> None:
        self.wrapper = 'wrapper'
        self.cmd_def = {
            'request_wrapper': self.wrapper
        }
        self.parameters = {'key': 'value'}
        self.request = BaseRequest('command', parameters=self.parameters)

    def test_wrap_request_without_wrapper(self):
        self.cmd_def.pop('request_wrapper')
        result = wrap_request(self.cmd_def, self.request)
        self.assertIs(result, self.request)
        self.assertEqual(result.parameters, self.parameters)

    def test_wrap_request_success(self):
        result = wrap_request(self.cmd_def, self.request)
        self.assertIs(result, self.request)
        self.assertEqual(result.parameters, {
            self.wrapper: self.parameters
        })


class TestVerifyResponse(unittest.TestCase):
    def setUp(self) -> None:
        self.response = MagicMock()
        self.content = 'content'
        self.response.content = self.content.encode()
        self.reason = 'common reason'
        self.response.raw.reason = self.reason
        self.text = 'text'
        self.response.text = self.text

    def test_verify_response_404(self):
        status_code = 404
        self.response.status_code = status_code
        with self.assertRaises(AssertionError) as context:
            verify_response(self.response)
        self.assertEqual(str(context.exception),
                         f'[{status_code}] Requested resource not found. '
                         f'{self.reason}')

    def test_verify_response_401(self):
        status_code = 401
        self.response.status_code = status_code
        with self.assertRaises(AssertionError) as context:
            verify_response(self.response)
        self.assertEqual(str(context.exception),
                         f'[{status_code}] '
                         f'Bad credentials. Please use the command '
                         f'"m3 access" to set up a valid credentials. '
                         f'Or try to install the latest version of m3 tool.')

    def test_verify_response_413(self):
        status_code = 413
        self.response.status_code = status_code
        self.response.json.return_value = {}
        with self.assertRaises(AssertionError) as context:
            verify_response(self.response)
        self.assertEqual(str(context.exception),
                         f'[{status_code}] Payload Too Large')

        message_text = 'message text'
        self.response.json.return_value = {'message': message_text}
        with self.assertRaises(AssertionError) as context:
            verify_response(self.response)
        self.assertEqual(str(context.exception),
                         f'[{status_code}] {message_text}')

    def test_verify_response_500(self):
        status_code = 500
        self.response.status_code = status_code
        with self.assertRaises(AssertionError) as context:
            verify_response(self.response)
        self.assertEqual(str(context.exception),
                         f'[{status_code}] Error during executing request. '
                         f'{self.reason}')

    def test_verify_response_not_status_code(self):
        self.response.status_code = None
        with self.assertRaises(AssertionError) as context:
            verify_response(self.response)
        self.assertEqual(str(context.exception),
                         f'[{204}] Empty response received. '
                         f'{self.reason}')

    def test_verify_response_not_200(self):
        status_code = 308
        self.response.status_code = status_code
        with self.assertRaises(AssertionError) as context:
            verify_response(self.response)
        self.assertEqual(str(context.exception),
                         f'[{status_code}] Error during executing request.'
                         f'Message: {self.text}')

    def test_verify_response_200(self):
        status_code = 200
        self.response.status_code = status_code
        result = verify_response(self.response)
        self.assertEqual(result, self.content)


class TestMaskParams(unittest.TestCase):
    def setUp(self) -> None:
        self.secured_params = ['API_KEY', 'password']
        self.input_value = "super secrets: 'API_KEY', 'password'"

    def test_mask_params_default_replace_value(self):
        expected_result = "super secrets: '*****', '*****'"
        result = mask_params(self.input_value, self.secured_params)
        self.assertEqual(result, expected_result)

    def test_mask_params_custom_replace_value(self):
        replace_value = 'a secret'
        expected_result = "super secrets: 'a secret', 'a secret'"
        result = mask_params(self.input_value, self.secured_params,
                             replace_value)
        self.assertEqual(result, expected_result)


class TestBaseRequest(unittest.TestCase):
    def setUp(self) -> None:
        self.request = BaseRequest(command='command',
                                   method='GET',
                                   parameters={'key': 'value'},
                                   api_action='API_ACTION')

    def test_base_request_repr(self):
        result = self.request.__repr__()
        self.assertEqual(result,
                         '{"command": "command", "api_action": "API_ACTION", '
                         '"parameters": {"key": "value"}, "method": "GET"}')

    def test_base_request_get_request(self):
        expected_result = {
            'command': 'command',
            'method': 'GET',
            'parameters': {
                'key': 'value'
            },
            'api_action': 'API_ACTION'
        }
        result = self.request.get_request()
        self.assertEqual(result, expected_result)


class TestSdkClientInit(TestSdkClient):
    def test_init_missed_secret_key(self):
        self.secret_key = ''
        with self.assertRaises(KeyError) as context:
            self.init_object_service()
        self.assertEqual(str(context.exception),
                         '\'Missed SECRET key for M3 SDK API. Please create '
                         'environment variable with name "M3SDK_SECRET_KEY" '
                         'and value that contains your valid '
                         'SDK SECRET Key.\'')

    def test_init_invalid_protocol(self):
        self.address = 'nothttp://address:port'
        with self.assertRaises(AssertionError) as context:
            self.init_object_service()
        self.assertEqual(str(context.exception),
                         f'Invalid URL: {self.address}. Please specify '
                         f'protocol.')


class TestSdkClientRequestParams(TestSdkClient):

    def test_request_params(self):
        result = self.service.request_params(self.requests)
        self.assertEqual(result[0], self.expected_unencrypted_object)
        self.assertEqual(result[1], self.expected_request_mapping)


class TestSdkClientExecute(TestSdkClient):
    def setUp(self) -> None:
        super().setUp()
        self.access_key = 'access_key'
        self.secret_key = '1234567890123456'

        self.executor = MagicMock()
        self.executors = {
            'POST': self.executor
        }
        expected_response = {
            'results': [{'result1': 'data'}]
        }  # the hash below is made specially from this expected_response
        self.expected_results = expected_response['results']
        response = MagicMock()
        response.status_code = 200
        response.content.decode.return_value = \
            '29YtdQUsWyFqM2WhLyVy+8MKtxsiZC/W4wv3CuFNPQgGVrMCmqVyL' \
            '8ynuFXzDnbmCdA='
        self.executor.return_value = response

        self.init_object_service()
        self.get_access_key_patch = patch(
            'm3cli.services.request_service.get_access_key',
            return_value=self.access_key)
        self.get_secret_key_patch = patch(
            'm3cli.services.request_service.get_secret_key',
            return_value=self.secret_key
        )
        self.executors_patch = patch(
            'm3cli.services.request_service.EXECUTORS',
            self.executors
        )
        self.get_access_key_patch.start()
        self.get_secret_key_patch.start()
        self.executors_patch.start()

    def test_execute_no_access_key(self):
        with patch('m3cli.services.request_service.get_access_key',
                   return_value=''):  # overrides the existing patch
            with self.assertRaises(KeyError) as context:
                self.service.execute(self.requests)
        self.assertEqual(str(context.exception),
                         '\'Missed ACCESS key for M3 SDK API. Please create '
                         'environment variable with name "M3SDK_ACCESS_KEY" '
                         'and value that contains your valid '
                         'SDK ACCESS Key.\'')

    def test_execute_connection_error(self):
        self.executor.side_effect = requests.ConnectionError
        with self.assertRaises(ConnectionError) as context:
            self.service.execute(self.requests)
        self.assertEqual(str(context.exception),
                         'Failed to establish new connection')

    # todo fix tests for a new encrypt-decrypt flow on m3-server
    # def test_execute_success(self):
    #     result = self.service.execute(self.requests)
    #     self.assertEqual(result[0], self.expected_request_mapping)
    #     self.assertEqual(result[1], self.expected_results)

    # def test_execute_execution_params(self):
    #     _ = self.service.execute(self.requests)
    #     self.assertTrue(len(self.executor.mock_calls) > 0)
    #     params = self.executor.mock_calls[0].kwargs
    #
    #     self.assertEqual(
    #         params.get('data'),
    #         self.service.signer.encrypt(json.dumps(
    #             self.expected_unencrypted_object)))
    #     self.assertEqual(params.get('url'), self.address)
    #
    #     headers = params.get('headers')
    #     self.assertEqual(headers.get('Content-Type'), 'application/json')
    #     self.assertEqual(headers.get('Accept'), 'application/json')
    #     self.assertIn('maestro-authentication', headers)
    #     self.assertEqual(headers.get('maestro-request-identifier'),
    #                      'api-server')
    #     self.assertEqual(headers.get('maestro-user-identifier'), 'SYSTEM')
    #     self.assertIn('maestro-date', headers)
    #     self.assertEqual(headers.get('maestro-accesskey'), self.access_key)
    #     self.assertIn('maestro-sdk-version', headers)
    #     self.assertEqual(headers.get('maestro-sdk-async'), 'false')
    #     self.assertIn('host', headers)

    def tearDown(self) -> None:
        self.get_access_key_patch.stop()
        self.get_secret_key_patch.stop()
        self.executors_patch.stop()


class TestSdkClientRequestMethod(TestSdkClient):
    def test_request_method(self):
        request = BaseRequest(command='command', method='POST')
        self.assertEqual(self.service.request_method([request]),
                         'POST')
