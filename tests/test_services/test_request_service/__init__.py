import unittest
from unittest.mock import patch

from m3cli.services.request_service import BaseRequest
from m3cli.services.request_service import SdkClient


class TestSdkClient(unittest.TestCase):
    def setUp(self) -> None:
        self.secret_key = '1234567890123456'
        self.address = 'https://address:port'
        self.service = SdkClient
        self.requests = [
            BaseRequest(command='command1', api_action='action1', parameters={
                'key': 'value'
            }),
            BaseRequest(command='command2', api_action='action2', parameters={
            })
        ]
        self.uuid_patch = patch('m3cli.services.request_service.uuid.uuid4',
                                side_effect=['1', '2'])
        self.expected_unencrypted_object = [
            {
                'id': '1',
                'type': 'ACTION1',
                'params': {
                    'body': '{"key": "value"}'
                }
            },
            {
                'id': '2',
                'type': 'ACTION2',
                'params': {
                    'body': None
                }
            }
        ]
        self.expected_request_mapping = {
            '1': self.requests[0],
            '2': self.requests[1]
        }
        self.uuid_patch.start()

    def tearDown(self) -> None:
        self.uuid_patch.stop()

    def init_object_service(self):
        with patch('m3cli.services.request_service.get_secret_key',
                   return_value=self.secret_key):
            with patch('m3cli.services.request_service.get_agent_address',
                       return_value=self.address):
                self.service = SdkClient()
