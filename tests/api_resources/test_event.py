from coinbase_commerce.api_resources.event import Event
from tests.base_test_case import BaseTestCase


class TestEvent(BaseTestCase):
    def test_list(self):
        # arrange
        self.stub_request('get', 'events', {'data': ['foo', 'bar']})
        # act
        event_list = self.client.event.list()
        # assert
        self.assert_requested('get', 'events', params={})
        self.assertIsInstance(event_list, Event)
        self.assertIsInstance(event_list.data, list)

    def test_list_iter(self):
        # arrange
        self.stub_request('get', 'events', {'data': list(range(20))})
        # act
        for event in self.client.event.list_paging_iter():
            # assert
            self.assertTrue(event in range(20))

    def test_list_iter_mapping(self):
        # arrange
        self.stub_request('get', 'events', {'data': [{'resource': 'event'} for _ in range(20)]})
        # act
        for event in self.client.event.list_paging_iter():
            # assert
            self.assertIsInstance(event, Event)

    def test_retrieve(self):
        data = {'item_id': 'foo', 'data': []}
        # arrange
        self.stub_request('get', 'events', data)
        # act
        event = self.client.event.retrieve('foo')
        # assert
        self.assert_requested('get', 'events', 'foo', params={})
        self.assertIsInstance(event, Event)
