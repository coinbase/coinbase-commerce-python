import unittest

import coinbase_commerce
from tests.request_mock import RequestMock

API_KEY = 'testkey'


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.request_mock = RequestMock()
        self.request_mock.start()
        self.client = coinbase_commerce.Client(API_KEY)

    def tearDown(self):
        super(BaseTestCase, self).tearDown()
        self.request_mock.stop()

    def stub_request(self, *args, **kwargs):
        return self.request_mock.stub_request(*args, **kwargs)

    def assert_requested(self, *args, **kwargs):
        return self.request_mock.assert_requested(*args, **kwargs)

    def assert_no_request(self):
        return self.request_mock.assert_no_request()
