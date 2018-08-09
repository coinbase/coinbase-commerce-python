from coinbase_commerce.api_resources.base import UpdateAPIResource
from tests.base_test_case import BaseTestCase


class TestUpdateResource(UpdateAPIResource):
    RESOURCE_PATH = "list_tests"


class TestUpdateAPIResource(BaseTestCase):

    def test_save(self):
        self.stub_request('put', TestUpdateResource.RESOURCE_PATH)
        TestUpdateResource._api_client = self.client
        obj = TestUpdateResource(data={'id': 'foo'})
        obj.baz = 'bar'
        obj.save()
        self.assert_requested('put', TestUpdateResource.RESOURCE_PATH, 'foo',
                              data={'baz': 'bar'})

    def test_save_fail_with_no_id(self):
        TestUpdateResource._api_client = self.client
        obj = TestUpdateResource(data={'name': 'baz'})
        obj.foo = 'bar'
        with self.assertRaises(ValueError):
            obj.save()
            self.assert_no_request()

    def test_modify(self):
        self.stub_request('put', TestUpdateResource.RESOURCE_PATH)
        TestUpdateResource._api_client = self.client
        TestUpdateResource.modify(entity_id='foo', baz='bar')
        self.assert_requested('put', TestUpdateResource.RESOURCE_PATH, 'foo',
                              data={'baz': 'bar'})
