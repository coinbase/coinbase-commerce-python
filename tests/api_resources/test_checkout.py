from coinbase_commerce.api_resources.checkout import Checkout
from tests.base_test_case import BaseTestCase


class TestCheckout(BaseTestCase):

    def test_list(self):
        # arrange
        self.stub_request('get', 'checkouts', {'data': ['foo', 'bar']})
        # act
        checkout = self.client.checkout.list()
        # assert
        self.assert_requested('get', 'checkouts', params={})
        self.assertIsInstance(checkout, Checkout)
        self.assertIsInstance(checkout.data, list)

    def test_list_iter(self):
        # arrange
        self.stub_request('get', 'checkouts', {'data': list(range(25))})
        # act
        for checkout in self.client.checkout.list_paging_iter():
            # assert
            self.assertTrue(checkout in range(25))

    def test_list_iter_mapping(self):
        # arrange
        self.stub_request('get', 'checkouts', {'data': [{'resource': 'checkout'} for _ in range(25)]})
        # act
        for checkout in self.client.checkout.list_paging_iter():
            # assert
            self.assertIsInstance(checkout, Checkout)

    def test_retrieve(self):
        # arrange
        checkout_data = {'id': 'bar'}
        self.stub_request('get', 'checkouts', checkout_data)
        # act
        checkout = self.client.checkout.retrieve(checkout_data.get('id'))
        # assert
        self.assert_requested('get', 'checkouts', checkout_data.get('id'), params={})
        self.assertIsInstance(checkout, Checkout)
        self.assertEqual(checkout.id, checkout_data.get('id'))

    def test_create(self):
        # arrange
        checkout_data = {'id': 'bar'}
        self.stub_request('post', 'checkouts', checkout_data)
        # act
        checkout = self.client.checkout.create(**checkout_data)
        # assert
        self.assert_requested('post', 'checkouts', data=checkout_data)
        self.assertIsInstance(checkout, Checkout)
        self.assertEqual(checkout.id, checkout_data.get('id'))

    def test_update_save(self):
        # arrange
        checkout_data = {'id': 'bar', 'name': 'foo'}
        self.stub_request('post', 'checkouts', checkout_data)
        checkout = self.client.checkout.create(**checkout_data)
        self.stub_request('put', 'checkouts', {'data': {'id': 'bar', 'name': 'new foo'}})
        # act
        checkout.name = 'new foo'
        checkout.save()
        # assert
        self.assert_requested('put', 'checkouts', 'bar', data={'name': 'new foo'})
        self.assertEqual(checkout.name, 'new foo')

    def test_update_modify(self):
        # arrange
        self.stub_request('put', 'checkouts', {'id': 'bar', 'name': 'new foo bar'})
        # act
        checkout = self.client.checkout.modify('bar', name='new foo bar')
        # assert
        self.assertIsInstance(checkout, Checkout)
        self.assert_requested('put', 'checkouts', 'bar', data={'name': 'new foo bar'})
        self.assertEqual(checkout.name, 'new foo bar')

    def test_delete(self):
        # arrange
        checkout_data = {'id': 'bar'}
        self.stub_request('post', 'checkouts', checkout_data)
        checkout = self.client.checkout.create(**checkout_data)
        checkout_id = checkout.id
        self.stub_request('delete', 'checkouts', {})
        # act
        checkout.delete()
        # assert
        self.assert_requested('delete', 'checkouts', checkout_id, data={})
        self.assertFalse(checkout)
