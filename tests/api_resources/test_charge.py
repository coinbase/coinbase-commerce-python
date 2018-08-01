from coinbase_commerce.api_resources.charge import Charge
from tests.base_test_case import BaseTestCase


class TestCharge(BaseTestCase):
    def test_list(self):
        # arrange
        self.stub_request('get', 'charges', {'data': ['boo', 'foo']})
        # act
        charge_list = self.client.charge.list()
        # assert
        self.assert_requested('get', 'charges', params={})
        self.assertIsInstance(charge_list, Charge)
        self.assertIsInstance(charge_list.data, list)

    def test_list_iter(self):
        # arrange
        self.stub_request('get', 'charges', {'data': list(range(20))})
        # act
        for charge in self.client.charge.list_paging_iter():
            # assert
            self.assertTrue(charge in range(20))

    def test_list_iter_mapping(self):
        # arrange
        self.stub_request('get', 'charges', {'data': [{'resource': 'charge'} for _ in range(20)]})
        # act
        for charge in self.client.charge.list_paging_iter():
            # assert
            self.assertIsInstance(charge, Charge)

    def test_retrieve(self):
        # arrange
        self.stub_request('get', 'charges', {'id': 'foo', 'code': 'bar'})
        # act
        resource = self.client.charge.retrieve('foo')
        # assert
        self.assert_requested('get', 'charges', 'foo', params={})
        self.assertIsInstance(resource, Charge)
        self.assertEqual(resource.id, 'foo')
        self.assertEqual(resource.code, 'bar')

    def test_create(self):
        # arrange
        charge_data = {'id': 'foo'}
        self.stub_request('post', 'charges', charge_data)
        # act
        resource = self.client.charge.create(**charge_data)
        # assert
        self.assert_requested('post', 'charges', data=charge_data)
        self.assertIsInstance(resource, Charge)
        self.assertEqual(resource.id, 'foo')
