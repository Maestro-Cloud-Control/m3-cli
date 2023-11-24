import unittest

from m3cli.utils.cloud_utils import Cloud, cloud_exist, assert_cloud_exist, \
    is_public


class TestCloudEnum(unittest.TestCase):
    def setUp(self) -> None:
        self.not_existing_cloud = 'NOT_EXISTING_CLOUD'

    def test_existing_clouds(self):
        expected_existing_clouds = {
            'AWS': False, 'AZURE': False, 'GOOGLE': False, 'YANDEX': False,
            'OPEN_STACK': True, 'HPOO': True, 'CSA': True, 'EXOSCALE': True,
            'HARDWARE': True, 'ENTERPRISE': True, 'VMWARE': True,
            'VSPHERE': True, 'NUTANIX': True, 'WORKSPACE': True, 'AOS': True
        }
        for entity in Cloud:
            self.assertIn(entity.name, expected_existing_clouds)
            self.assertEqual(entity.name, entity.cloud_name)
            self.assertEqual(entity.is_private,
                             expected_existing_clouds[entity.name])
            expected_existing_clouds.pop(entity.name)
        if expected_existing_clouds:
            self.fail(f'These parameters: {expected_existing_clouds} are '
                      f'supposed to be in Cloud Enum')

    def test_cloud_exists(self):
        self.assertTrue(cloud_exist('AWS'))
        self.assertTrue(cloud_exist('AZURE'))
        self.assertTrue(cloud_exist('GOOGLE'))

        self.assertFalse(cloud_exist(self.not_existing_cloud))

    def test_assert_cloud_exists(self):
        try:
            assert_cloud_exist('AWS')
        except Exception as e:
            self.fail(f'Exception {e} wasn\'t supposed to be here')

        with self.assertRaises(AssertionError) as context:
            assert_cloud_exist(self.not_existing_cloud)
        self.assertEqual(str(context.exception),
                         f'Cloud \'{self.not_existing_cloud}\' does not '
                         f'exists')

    def test_is_public(self):
        self.assertTrue(is_public('AWS'))
        self.assertTrue(is_public('AZURE'))
        self.assertTrue(is_public('GOOGLE'))
        self.assertFalse(is_public('OPEN_STACK'))
        self.assertFalse(is_public('HPOO'))
        self.assertFalse(is_public('CSA'))

        with self.assertRaises(AssertionError) as context:
            is_public(self.not_existing_cloud)
        self.assertEqual(str(context.exception),
                         f'Cloud \'{self.not_existing_cloud}\' does not '
                         f'exists')
