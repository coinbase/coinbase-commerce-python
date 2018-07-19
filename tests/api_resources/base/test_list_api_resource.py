from coinbase_commerce.api_resources import Charge
from coinbase_commerce.api_resources.base import ListAPIResource
from tests.base_test_case import BaseTestCase


class TestDeleteResource(ListAPIResource):
    RESOURCE_PATH = "list_tests"


class TestListAPIResource(BaseTestCase):

    def test_list(self):
        self.stub_request('get', TestDeleteResource.RESOURCE_PATH,
                          {'data': [{'resource': 'charge', 'name': 'foo', },
                                    {'resource': 'charge', 'name': 'bar', }], }, )
        TestDeleteResource._api_client = self.client
        res = TestDeleteResource.list()
        self.assert_requested('get', TestDeleteResource.RESOURCE_PATH, params={})
        self.assertEqual(2, len(res.data))
        self.assertTrue(all(isinstance(obj, Charge)
                            for obj in res.data))
        self.assertEqual('foo', res.data[0].name)
        self.assertEqual('bar', res.data[1].name)
