from coinbase_commerce.api_resources.base import APIResource
from tests.base_test_case import BaseTestCase


class TestResource(APIResource):
    RESOURCE_PATH = "tests"


class TestAPIResource(BaseTestCase):

    def test_retrieve(self):
        TestResource._api_client = self.client
        self.stub_request('get', TestResource.RESOURCE_PATH, {'id': 'foo', 'name': 'bar', })
        res_obj = TestResource.retrieve('foo', test_param=42)
        self.assert_requested('get', 'tests', 'foo', params={'test_param': 42})
        self.assertEqual('bar', res_obj.name)
        self.assertEqual('foo', res_obj.id)
        self.stub_request('get', TestResource.RESOURCE_PATH)

    def test_refresh(self):
        TestResource._api_client = self.client
        self.stub_request('get', TestResource.RESOURCE_PATH, {'id': 'foo', 'name': 'bar', })
        res_obj = TestResource.retrieve('foo', test_param=42)
        self.stub_request('get', TestResource.RESOURCE_PATH, {'id': 'foo'})
        refreshed = res_obj.refresh()
        self.assert_requested('get', 'tests', 'foo')
        self.assertEqual(res_obj, refreshed)

    def test_refresh_fail_with_no_id(self):
        TestResource._api_client = self.client
        self.stub_request('get', TestResource.RESOURCE_PATH, {'name': 'bar', })
        res_obj = TestResource.retrieve('foo', test_param=42)
        with self.assertRaises(ValueError):
            res_obj.refresh()
            self.assert_no_request()

    def test_subclasses(self):
        self.assertIn(TestResource, APIResource.get_subclasses())
