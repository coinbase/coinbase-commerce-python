import json
import warnings


class CoinbaseResponse(object):
    """
    Representation for coinbase commerce response object
    """

    def __init__(self, body, code, headers):

        # in case of py27, py34
        if isinstance(body, bytes):
            body = body.decode('utf-8')

        self.body = body
        self.code = code
        self.headers = headers
        self.data = json.loads(body)
        self.proceed_warnings()

    @property
    def request_id(self):
        return self.headers.get('x-request-id')

    def proceed_warnings(self):
        warnings_data = self.data.get('warnings', [])
        for warning_message in warnings_data:
            warnings.warn(warning_message, UserWarning)
