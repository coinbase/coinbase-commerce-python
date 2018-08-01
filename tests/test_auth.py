import mock
from coinbase_commerce.auth import APIAuth
from tests.base_test_case import BaseTestCase


class TestAuth(BaseTestCase):

    def test_auth_init(self):
        auth = APIAuth('foo', 'bar')
        self.assertEqual(auth.api_key, 'foo')
        self.assertEqual(auth.api_version, 'bar')

    def test_auth_call(self):
        auth = APIAuth('foo', 'bar')
        mock_request = mock.MagicMock
        mock_request.headers = {}
        auth(mock_request)
        self.assertTrue(mock_request.headers.get('X-CC-Api-Key'))
        self.assertTrue(mock_request.headers.get('X-CC-Version'))
        self.assertEqual(mock_request.headers['X-CC-Api-Key'], 'foo')
        self.assertEqual(mock_request.headers['X-CC-Version'], 'bar')
