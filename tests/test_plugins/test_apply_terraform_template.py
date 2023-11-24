from tests.test_plugins import TestPluginsBase


class TestApplyTerraformTemplate(TestPluginsBase):
    PLUGIN_NAME = 'apply-terraform-template'

    def test_apply_terraform_template_request_without_variables_success(self):
        self.request.parameters = {
            'task': 'anything'
        }

        result = self.execute_create_custom_request()
        self.assertEqual(result.parameters['task'], 'PLAN')

    def test_apply_terraform_template_request_with_list_variables_success(self):
        self.request.parameters = {
            'variables': {
                'some_name': '1,3',
            }
        }

        expected_result = {
            'some_name': {
                'type': 'LIST',
                'value': ['1', '3'],
                'sensitive': True,
                'name': 'some_name'
            }
        }

        result = self.execute_create_custom_request()
        self.assertEqual(result.parameters['variables'], expected_result)

    def test_apply_terraform_template_request_with_map_variables_success(self):
        self.request.parameters = {
            'variables': {
                'some_name': 'sixteen=16',
            }
        }

        expected_result = {
            'some_name': {
                'type': 'MAP',
                'value': {'sixteen': '16'},
                'sensitive': True,
                'name': 'some_name'
            }
        }

        result = self.execute_create_custom_request()
        self.assertEqual(result.parameters['variables'], expected_result)

    def test_apply_terraform_template_request_with_string_variables_success(self):
        self.request.parameters = {
            'variables': {
                'some_name': 'some_string',
            }
        }

        expected_result = {
            'some_name': {
                'type': 'STRING',
                'value': 'some_string',
                'sensitive': True,
                'name': 'some_name'
            }
        }

        result = self.execute_create_custom_request()
        self.assertEqual(result.parameters['variables'], expected_result)
