from coinbase_commerce.api_resources.base import APIResource
from coinbase_commerce.util import (
    RESOURCE_MAP,
    clean_params,
    register_resource_cls,
)
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

    def test_register_resource_cls(self):
        # test not for unsupported classes
        with self.assertRaises(TypeError):
            @register_resource_cls
            class Foo(object):
                pass

        # Call decorator with invalid positional argument
        with self.assertRaises(TypeError):
            @register_resource_cls('something')
            class Bar(APIResource):
                RESOURCE_PATH = "bars"
                RESOURCE_NAME = "bar"

        # Call decorator with both positional and keyword arguments
        with self.assertRaises(ValueError):
            @register_resource_cls('something', resource_name_default="baz")
            class Baz(APIResource):
                RESOURCE_PATH = "bazs"
                RESOURCE_NAME = "baz"

        # Not call decorator
        RESOURCE_MAP.clear()

        @register_resource_cls
        class NotCall(APIResource):
            RESOURCE_PATH = "not_calls"
            RESOURCE_NAME = "not_call"

        assert "not_call" in RESOURCE_MAP

        # Call decorator with keyword argument only
        RESOURCE_MAP.clear()

        @register_resource_cls(resource_name_default="with_keyword")
        class WithKeyword(APIResource):
            RESOURCE_PATH = "with_keywords"

        assert "with_keyword" in RESOURCE_MAP

        # Call decorator with keyword argument
        # for class with declared class var
        RESOURCE_MAP.clear()

        @register_resource_cls(resource_name_default="with_keyword_class_var")
        class WithKeywordAndClassVar(APIResource):
            RESOURCE_PATH = "with_keyword_and_class_vars"
            RESOURCE_NAME = "with_keyword_and_class_var"

        assert "with_keyword_class_var" not in RESOURCE_MAP
        assert "with_keyword_and_class_var" in RESOURCE_MAP
