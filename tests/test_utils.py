from coinbase_commerce.util import clean_params
from tests.base_test_case import BaseTestCase


class TestUtils(BaseTestCase):
    def test_clean_params(self):
        input = {
            'none': None,
            'int': 1,
            'float': 2.0,
            'bool': True,
            'nested': {
                'none': None,
                'int': 1,
                'float': 2.0,
                'bool': False,
            },
        }

        self.assertEqual(clean_params(input), {
            'int': 1,
            'float': 2.0,
            'bool': True,
            'nested': {
                'int': 1,
                'float': 2.0,
                'bool': False,
            },
        })
        self.assertEqual(clean_params(input, drop_nones=False), {
            'none': None,
            'int': 1,
            'float': 2.0,
            'bool': 1,
            'nested': {
                'none': None,
                'int': 1,
                'float': 2.0,
                'bool': 0,
            },
        })
        self.assertEqual(clean_params(input, recursive=False), {
            'int': 1,
            'float': 2.0,
            'bool': 1,
            'nested': {
                'none': None,
                'int': 1,
                'float': 2.0,
                'bool': 0,
            },
        })
