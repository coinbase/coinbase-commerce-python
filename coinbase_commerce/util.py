import functools
import hmac
import json
import warnings

import six

from coinbase_commerce.compat import urlparse
from coinbase_commerce.response import CoinbaseResponse

RESOURCE_MAP = {}


def register_resource_cls(*args, **kwargs):
    """Class decorator for registering API resource classes"""
    # to avoid a circular dependency
    from coinbase_commerce.api_resources.base import APIResource

    def resource_decorator(cls, resource_name_default=None):
        if not issubclass(cls, APIResource):
            raise TypeError(
                "only {!r} subclasses are supported".format(APIResource)
            )

        rn = getattr(cls, "RESOURCE_NAME", resource_name_default)
        if rn is not None:
            RESOURCE_MAP[rn] = cls
        return cls

    if args and kwargs:
        raise ValueError("cannot combine positional and keyword args")
    if len(args) == 1:
        return resource_decorator(args[0])
    elif len(args) != 0:
        raise ValueError("expected 1 argument, got %d", len(args))
    return functools.partial(resource_decorator, **kwargs)


def load_resource_map():
    """
    Create APIResources class mapping
    {str : Class}
    """
    # to avoid a circular dependency
    from coinbase_commerce.api_resources.base import APIResource

    RESOURCE_MAP.update({
        k.RESOURCE_NAME: k
        for k in APIResource.get_subclasses()
        if hasattr(k, "RESOURCE_NAME")
    })


def clean_params(params, drop_nones=True, recursive=True):
    """Clean up a dict of API parameters to be sent to the Coinbase API."""
    cleaned = {}
    for key, value in params.items():
        if drop_nones and value is None:
            continue
        if recursive and isinstance(value, dict):
            value = clean_params(value, drop_nones, recursive)
        cleaned[key] = value
    return cleaned


def encode_params(params, **kwargs):
    """Clean and JSON-encode a dict of parameters."""
    cleaned = clean_params(params, **kwargs)
    return json.dumps(cleaned)


def check_uri_security(uri):
    """Warns if the URL is insecure."""
    if urlparse(uri).scheme != 'https':
        warning_message = (
            'WARNING: this client is sending a request to an insecure '
            'API endpoint. Any API request you make may expose your API key '
            'and secret to third parties. Consider using the default '
            'endpoint:\n\n '
            '{}\n'.format(uri)
        )
        warnings.warn(warning_message, UserWarning)
    return uri


def convert_to_api_object(response, api_client=None, resource_class=None):
    """Convert Commerce response to valid python object"""

    def get_klass(response):
        """
        get APIResponse class or class from params
        if both are None returns APIObject
        """
        # to avoid a circular dependency
        from coinbase_commerce.api_resources.base import APIObject
        try:
            from coinbase_commerce.aio import Client as AsyncClient
        except (ImportError, SyntaxError):
            AsyncClient = None  # noqa

        if not RESOURCE_MAP:
            load_resource_map()

        klass_name = response.get('resource')
        if isinstance(klass_name, str):
            if AsyncClient is not None and isinstance(api_client, AsyncClient):
                klass_name += '_aio'

        klass = RESOURCE_MAP.get(klass_name) or resource_class

        # provide api_client only for resource classes
        return (
            klass(api_client=api_client, data=response)
            if klass else APIObject(data=response)
        )

    if isinstance(response, CoinbaseResponse):
        response = response.data

        # unpack nested data field
        if isinstance(response.get('data'), dict):
            data = response.pop('data', None)
            response.update(data)

    if isinstance(response, list):
        return [
            convert_to_api_object(item, api_client=api_client)
            for item in response
        ]

    if isinstance(response, dict):
        return get_klass(response)

    return response


def secure_compare(a, b):
    """
    Return 'a == b'.  This function uses an approach designed to prevent
    timing analysis, making it appropriate for cryptography.
    a and b must both be of the same type: either str (ASCII only),
    or any bytes-like object.
    """

    def utf8(value):
        if six.PY2 and isinstance(value, six.text_type):
            return value.encode('utf-8')
        else:
            return value

    return hmac.compare_digest(utf8(a), utf8(b))


class lazy_property(object):
    """ Meant to be used for lazy evaluation of an object attribute."""

    def __init__(self, fget):
        self.fget = fget

        # copy the getter function's docstring and other attributes
        functools.update_wrapper(self, fget)

    def __get__(self, obj, cls):
        if obj is None:
            return self

        value = self.fget(obj)
        setattr(obj, self.fget.__name__, value)
        return value
