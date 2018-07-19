from coinbase_commerce.error import APIError
from tests.base_test_case import BaseTestCase


class TestApiError(BaseTestCase):

    def test_no_request_error_formatting(self):
        err = APIError('bar')
        self.assertEqual('bar', str(err))

    def test_request_provided_error_formatting(self):
        err = APIError('foo', headers={'X-Request-Id': 'bar'})
        self.assertEqual('Request id bar: foo', str(err))

    def test_request_provided_error_no_message_formatting(self):
        err = APIError(None, headers={'X-Request-Id': 'bar'})
        self.assertEqual('Request id bar: <empty message>', str(err))

    def test_no_request_no_message_formatting(self):
        err = APIError(None)
        self.assertEqual('<empty message>', str(err))
