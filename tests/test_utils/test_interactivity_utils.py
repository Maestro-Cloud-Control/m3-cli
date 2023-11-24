import unittest
from types import GeneratorType

from m3cli.models.interactive_parameter import InteractiveParameter
from m3cli.utils.interactivity_utils import get_interactivity_option, \
    unavailable_values_detector


class TestInteractivityUtilsGetInteractivityOption(unittest.TestCase):
    def setUp(self) -> None:
        self.option_name, self.option_value = 'option_name', 'option_value'
        self.interactivity_options = {
            self.option_name: self.option_value
        }

    def test_get_interactivity_option_required(self):
        self.interactivity_options.pop(self.option_name)
        with self.assertRaises(AssertionError) as context:
            get_interactivity_option(self.interactivity_options,
                                     self.option_name, required=True)
        self.assertEqual(str(context.exception),
                         f'{self.option_name} in not specified')

    def test_get_interactivity_option_not_required(self):
        result = get_interactivity_option(self.interactivity_options,
                                          self.option_name, required=False)
        self.assertEqual(result, self.option_value)
        self.interactivity_options.pop(self.option_name)
        result = get_interactivity_option(self.interactivity_options,
                                          self.option_name, required=False)
        self.assertIsNone(result)


class TestUnavailableValuesDetector(unittest.TestCase):
    def test_unavailable_values_detector(self):
        param_without_value = InteractiveParameter({'name': 'param1',
                                                    'type': 'LIST'})
        param_available = InteractiveParameter({'name': 'param2',
                                                'value': 'value',
                                                'type': 'LIST'})
        param_with_none_by_user = InteractiveParameter({'name': 'param3',
                                                        'type': 'LIST'})
        param_with_none_by_user.value = None
        parameters = [param_without_value, param_available,
                      param_with_none_by_user]
        result = unavailable_values_detector(parameters)
        self.assertIsInstance(result, GeneratorType)
        self.assertEqual(list(result), [param_without_value,
                                        param_with_none_by_user])
