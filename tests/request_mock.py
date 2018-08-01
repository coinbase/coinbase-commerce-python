import json
from mock import patch, ANY

import coinbase_commerce
from coinbase_commerce.response import CoinbaseResponse


class RequestMock(object):
    def __init__(self):
        self._stub_request_handler = RequestStub()
        self._real_coinbase_request = coinbase_commerce.Client._request
        self.request_patcher = patch(
            'coinbase_commerce.Client._request',
            side_effect=self._patched_request,
            autospec=True)

    def start(self):
        self.request_spy = self.request_patcher.start()

    def stop(self):
        self.request_patcher.stop()

    def _patched_request(self, api_client, method, url, *args, **kwargs):
        response = self._stub_request_handler.get_response(method, url)
        return response or self._real_coinbase_request(api_client, method, url,
                                                       *args, **kwargs)

    def stub_request(self, method, url, body=None, code=200, headers=None):
        self._stub_request_handler.register(method, url, body or {}, code,
                                            headers or {})

    def assert_requested(self, method, *relative_path_parts, **kwargs):
        self.request_spy.assert_called_with(ANY, method, *relative_path_parts, **kwargs)

    def assert_no_request(self):
        if self.request_spy.call_count != 0:
            msg = "Expected 'request' to not have been called." \
                  "Called {} times.".format(self.request_spy.call_count)
            raise AssertionError(msg)

    def reset_mock(self):
        self.request_spy.reset_mock()


class RequestStub(object):
    def __init__(self):
        self._entries = {}

    def register(self, method, url, body=None, code=200, headers=None):
        key = (method, url)
        value = (body or {}, code, headers or {})
        if self._entries.get(key):
            self._entries[key].append(value)
        else:
            self._entries[key] = [value]

    def get_response(self, method, url):
        key = (method, url)
        if self._entries.get(key):
            body, code, headers = self._entries[key].pop(0)
            if not isinstance(body, str):
                body = json.dumps(body)
            return CoinbaseResponse(body=body, code=code, headers=headers)
        return None
