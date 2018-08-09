import json

from coinbase_commerce import convert_to_api_object
from coinbase_commerce.api_resources.base.api_object import APIObject
from tests.base_test_case import BaseTestCase


class TestApiObject(BaseTestCase):

    def test_init(self):
        dummy = {"code": "foo", "name": "bar"}
        api_object = APIObject(data=dummy)
        self.assertEqual(api_object.code, dummy['code'])

    def test_access(self):
        dummy = {'foo': 'bar'}
        # Every key in the object should be accessible by attribute access.
        obj = convert_to_api_object(dummy)
        for key, value in dummy.items():
            assert (key in obj) and hasattr(obj, key)
            assert getattr(obj, key) is obj[key]

        # If a key is not in the object, it should not be accessible by attribute
        # access. It should raise AttributeError when access is attempted by
        # attribute instead of by key.
        broken_key = 'broken'
        assert broken_key not in obj
        assert not hasattr(obj, broken_key)
        with self.assertRaises(KeyError):
            obj[broken_key]
        with self.assertRaises(AttributeError):
            getattr(obj, broken_key)
        with self.assertRaises(KeyError):
            del obj[broken_key]
        with self.assertRaises(KeyError):
            delattr(obj, broken_key)

        # Methods on the object should not be accessible via key.
        data = {'foo': 'bar'}
        data_obj = convert_to_api_object(data)
        assert hasattr(data_obj, 'refresh_from')
        assert 'refresh_from' not in data_obj
        with self.assertRaises(KeyError):
            data_obj['refresh_from']

        # Setting attributes that begin with a '_' are not available via __getitem__
        data_obj._test = True
        self.assertEqual(getattr(data_obj, '_test', None), True)
        self.assertEqual(data_obj.get('_test', None), None)

        # Setting attribuets that don't begin with a '_' are available via __getitem__
        data_obj.test = True
        self.assertEqual(getattr(data_obj, 'test', None), True)
        self.assertEqual(data_obj.get('test', None), True)

    def test_new_api_object_uses_cls_if_available(self):
        class Foo(APIObject):
            pass

        obj = convert_to_api_object({'id': 'foo'},
                                    resource_class=Foo)
        self.assertIsInstance(obj, Foo)

    def test_new_api_object_guesses_based_on_resource_field(self):
        class Foo(APIObject):
            RESOURCE_NAME = 'foo'

        import coinbase_commerce
        coinbase_commerce.util.RESOURCE_MAP[Foo.RESOURCE_NAME] = Foo
        obj = convert_to_api_object({'resource': 'foo'})
        self.assertIsInstance(obj, Foo)

    def test_new_api_object_transforms_types_appropriately(self):
        dummy = {'obj': {'obj': {'foo': 'bar'}},
                 'list_of_objs': [{'foo': 'bar'}, {'bar': 'foo'}],
                 'str': 'foo',
                 'int': 1,
                 'float': .1,
                 'bool': True,
                 'none': None}
        simple_obj = convert_to_api_object(dummy)

        # Check root level for dict -> APIObject transformation.
        self.assertIsInstance(dummy['obj'], dict)
        self.assertIsInstance(simple_obj['obj'], APIObject)

        # Check the second level for dict -> APIObject transformation.
        self.assertIsInstance(dummy['obj']['obj'], dict)
        self.assertIsInstance(simple_obj['obj']['obj'], APIObject)

        # Check lists for dict -> APIObject transformation
        self.assertIsInstance(dummy['list_of_objs'], list)
        self.assertIsInstance(simple_obj['list_of_objs'], list)
        for item in dummy['list_of_objs']:
            self.assertIsInstance(item, dict)
        for item in simple_obj['list_of_objs']:
            self.assertIsInstance(item, APIObject)

        # Check that non-dict/list values are left the same.
        self.assertIsInstance(dummy['str'], str)
        self.assertIsInstance(simple_obj['str'], str)
        self.assertIsInstance(dummy['int'], int)
        self.assertIsInstance(simple_obj['int'], int)
        self.assertIsInstance(dummy['float'], float)
        self.assertIsInstance(simple_obj['float'], float)
        self.assertIsInstance(dummy['bool'], bool)
        self.assertIsInstance(simple_obj['bool'], bool)
        self.assertIsNone(dummy['none'])
        self.assertIsNone(simple_obj['none'])

    def test_json_serialization(self):
        dummy = {'obj': {'obj': {'foo': 'bar'}},
                 'list_of_objs': [{'foo': 'bar'}, {'bar': 'foo'}]}

        simple_obj = convert_to_api_object(response=dummy)

        # APIObjects should be equivalent to the dicts from which they were loaded.
        self.assertEqual(simple_obj, dummy)

        # APIObjects should be JSON-serializable; the serialized version should be
        # identical to the serialized version of the data from which the object
        # was originally created.
        json_data = json.dumps(dummy, sort_keys=True)
        json_obj = json.dumps(simple_obj, sort_keys=True)
        self.assertEqual(json_data, json_obj)

        # Two APIObjects created from the same data should be equivalent.
        simple_obj2 = convert_to_api_object(response=dummy)
        self.assertEqual(simple_obj, simple_obj2)

        # When an object is unserializable, it should still be convertible to a
        # string.
        from decimal import Decimal
        broken_obj = convert_to_api_object(response={'cost': Decimal('12.0')})
        self.assertTrue(str(broken_obj).endswith('(invalid JSON)'))

    def test_api_object_has_no_client_relation(self):
        api_client = lambda x: x

        class Foo(APIObject):
            RESOURCE_NAME = 'foo'

        import coinbase_commerce
        coinbase_commerce.util.RESOURCE_MAP[Foo.RESOURCE_NAME] = Foo
        foo_obj = convert_to_api_object(api_client=api_client, response={'resource': 'foo'})

        api_obj = convert_to_api_object(api_client=api_client, response={'resource': 'bar'})
        self.assertIsInstance(foo_obj, Foo)
        self.assertIsInstance(api_obj, APIObject)
        self.assertIs(foo_obj._api_client, api_client)
        self.assertIsNone(api_obj._api_client)

    def test_refresh_from(self):
        obj = convert_to_api_object(response={'foo': 'bar', 'trans': 'me'})
        self.assertEqual('bar', obj.foo)
        self.assertEqual('me', obj['trans'])
        obj.refresh_from(**{'foo': 'baz', 'johnny': 5, })
        self.assertEqual(5, obj.johnny)
        self.assertEqual('baz', obj.foo)
        self.assertRaises(AttributeError, getattr, obj, 'trans')
        obj.refresh_from(**{'trans': 4, 'metadata': {'amount': 42}})
        self.assertRaises(AttributeError, getattr, obj, 'foo')
        self.assertEqual(4, obj.trans)

    def test_repr(self):
        obj = APIObject(data={'foo': 'bar', 'id': 'boo'})
        obj['object'] = u'\u4e00boo\u1f00'
        res = repr(obj)
        self.assertTrue('<APIObject' in res)
        self.assertTrue('id=boo' in res)

    def test_serialize(self):
        obj = APIObject(data={'foo': 'bar', 'id': 'boo', 'dummy': APIObject(data={'test': 'boo'})})
        obj.baz = 'bar'
        obj.dummy.test = 'foo'
        serialized = obj.serialize()
        self.assertTrue(serialized.get('baz'))
        self.assertTrue(serialized.get('dummy'))
        self.assertIsNone(serialized.get('foo'))
        self.assertIsInstance(serialized.get('dummy'), APIObject)

    def test_update(self):
        obj = APIObject(data={'foo': 'bar', 'id': 'boo'})
        obj.update({'baz': 'bar'})
        self.assertIn('baz', obj._unsaved_values)

    def test_unsaved(self):
        obj = APIObject(data={'foo': 'bar', 'id': 'boo'})
        obj.baz = 'bar'
        self.assertIn('baz', obj._unsaved_values)
        del obj.baz
        self.assertFalse(obj._unsaved_values)
