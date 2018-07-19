from coinbase_commerce.api_resources.base import DeleteAPIResource
from tests.base_test_case import BaseTestCase


class TestDeleteResource(DeleteAPIResource):
    RESOURCE_PATH = "delete_tests"


class TestDeletableAPIResource(BaseTestCase):
    def test_delete(self):
        self.stub_request('delete', TestDeleteResource.RESOURCE_PATH,
                          {'id': 'foo', 'deleted': True}, )
        TestDeleteResource._api_client = self.client
        obj = TestDeleteResource(data={'id': 'foo', 'deleted': True})
        obj.delete()
        self.assert_requested('delete', TestDeleteResource.RESOURCE_PATH, 'foo', data={})
        self.assertEqual(True, obj.deleted)
        self.assertEqual('foo', obj.id)

    def test_delete_fails_with_no_id(self):
        TestDeleteResource._api_client = self.client
        obj = TestDeleteResource(data={'foo': 'bar'})
        with self.assertRaises(ValueError):
            obj.delete()
            self.assert_no_request()
