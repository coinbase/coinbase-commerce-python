import json
import warnings

from coinbase_commerce.response import CoinbaseResponse
from tests.base_test_case import BaseTestCase


class TestResponse(BaseTestCase):
    @staticmethod
    def mock_response(with_warn=False):
        code = 200
        headers = {'x-request-id': 'req_123456'}
        body = TestResponse.mock_body(with_warn)
        response = CoinbaseResponse(body, code, headers)
        return response, headers, body, code

    @staticmethod
    def mock_body(with_warn=False):
        response = {"data": {'foo': 'bar'}}
        if with_warn:
            response.update({"warnings": ["warning raises"]})
            return json.dumps(response)
        return json.dumps(response)

    def test_request_id(self):
        response, headers, body, code = TestResponse.mock_response()
        self.assertEqual(response.request_id, headers['x-request-id'])

    def test_code(self):
        response, headers, body, code = TestResponse.mock_response()
        self.assertEqual(response.code, code)

    def test_headers(self):
        response, headers, body, code = TestResponse.mock_response()
        self.assertEqual(response.headers, headers)

    def test_body(self):
        response, headers, body, code = TestResponse.mock_response()
        self.assertEqual(response.body, body)

    def test_data(self):
        response, headers, body, code = TestResponse.mock_response()
        self.assertEqual(response.data, json.loads(body))

    def test_warning(self):
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
            TestResponse.mock_response(with_warn=True)
            self.assertEqual(len(warning), 1)
            self.assertTrue(issubclass(warning[-1].category, UserWarning))
            self.assertTrue("warning raises" in str(warning[-1].message))
