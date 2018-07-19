from coinbase_commerce.api_resources import Checkout
from coinbase_commerce.api_resources.base import CreateAPIResource
from tests.base_test_case import BaseTestCase


class TestCreateResource(CreateAPIResource):
    RESOURCE_PATH = "create_tests"


class TestCreateAPIResource(BaseTestCase):

    def test_create(self):
        self.stub_request('post', TestCreateResource.RESOURCE_PATH,
                          {'resource': 'checkout', 'foo': 'bar', })
        TestCreateResource._api_client = self.client
        api_obj = TestCreateResource.create()
        self.assert_requested('post', TestCreateResource.RESOURCE_PATH, data={})
        self.assertEqual('bar', api_obj.foo)
        self.assertIsInstance(api_obj, Checkout)
