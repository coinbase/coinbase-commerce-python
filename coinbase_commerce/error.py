class CoinbaseError(Exception):
    """
    Base error class for all exceptions raised in this library.
    """
    pass


class SignatureVerificationError(CoinbaseError):
    """
    Raised for webhook signature verification failure
    """

    def __init__(self, sig_header=None, payload=None):
        if sig_header or payload:
            self._message = "No signatures found matching the expected signature " \
                            "{0} for payload {1}".format(sig_header, payload)
        else:
            self._message = "<empty message>"

    def __str__(self):
        return self._message


class APIError(CoinbaseError):
    """
    Raised for errors related to interacting with the Coinbase API server.
    """

    def __init__(self,
                 message=None,
                 http_body=None,
                 http_status=None,
                 json_body=None,
                 headers=None):
        super().__init__(message)

        self._message = message
        self.http_body = self.process_http_body(http_body)
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}
        self.request_id = self.headers.get('X-Request-Id', None)

    def process_http_body(self, http_body):
        if http_body and hasattr(http_body, 'decode'):
            try:
                http_body = http_body.decode('utf-8', 'strict')
            except Exception:
                http_body = ('<Could not decode body as utf-8. '
                             'Please report to commerce team')
        return http_body

    def __str__(self):
        msg = self._message or "<empty message>"
        if self.request_id is not None:
            return "Request id {0}: {1}".format(self.request_id, msg)
        else:
            return msg


class ParamRequiredError(APIError):
    pass


class ResourceNotFoundError(APIError):
    pass


class ValidationError(APIError):
    pass


class InvalidRequestError(APIError):
    pass


class AuthenticationError(APIError):
    pass


class InvalidTokenError(APIError):
    pass


class RateLimitExceededError(APIError):
    pass


class InternalServerError(APIError):
    pass


class ServiceUnavailableError(APIError):
    pass


class WebhookInvalidPayload(APIError):
    pass


def build_api_error(response, blob=None):
    """
    Helper method for creating errors and attaching HTTP response/request
    details to them.
    """
    blob = blob or response.json()
    error = getattr(blob, 'error', None) or blob.get('error', None)
    error_id = error.get('type', '')
    error_message = error.get('message', '')
    error_class = (_error_id_to_class.get(error_id, None) or
                   _status_code_to_class.get(response.status_code, APIError))

    return error_class(message=error_message,
                       http_body=response.content,
                       http_status=response.status_code,
                       json_body=blob,
                       headers=response.headers)


_error_id_to_class = {
    'not_found': ResourceNotFoundError,
    'param_required': ParamRequiredError,
    'validation_error': ValidationError,
    'invalid_request': InvalidRequestError,
    'authentication_error': AuthenticationError,
    'rate_limit_exceeded': RateLimitExceededError,
    'internal_server_error': InternalServerError,
}

_status_code_to_class = {
    400: InvalidRequestError,
    401: AuthenticationError,
    404: ResourceNotFoundError,
    429: RateLimitExceededError,
    500: InternalServerError,
    503: ServiceUnavailableError,
}
