from coinbase_commerce.compat import py2_unicode_compatible


@py2_unicode_compatible
class CoinbaseError(Exception):
    """
    Base error class for all exceptions raised in this library.
    """

    def __str__(self):
        msg = self._message or "<empty message>"
        request_id = getattr(self, "request_id", None)
        if request_id is not None:
            return u"Request id {0}: {1}".format(request_id, msg)
        else:
            return msg


class SignatureVerificationError(CoinbaseError):
    """
    Raised for webhook signature verification failure
    """

    def __init__(self, sig_header=None, payload=None):
        if sig_header or payload:
            self._message = u"No signatures found matching the expected signature " \
                            u"{0} for payload {1}".format(sig_header, payload)
        else:
            self._message = u"<empty message>"


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
        super(APIError, self).__init__(message)

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
                http_body = (u'<Could not decode body as utf-8. '
                             u'Please report to commerce team')
        return http_body


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
