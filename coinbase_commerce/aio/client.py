from aiohttp import ClientSession, ClientResponseError

from coinbase_commerce import Client as SyncClient
from coinbase_commerce.auth import APIAuthHeadersMixin
from coinbase_commerce.error import _build_api_error
from coinbase_commerce.response import CoinbaseResponse
from coinbase_commerce.util import encode_params, lazy_property
from .api_resources.charge import Charge
from .api_resources.checkout import Checkout
from .api_resources.event import Event


__all__ = (
    'Client',
)


class Client(SyncClient):
    DEFAULT_HEADERS = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Set api resource relations. with lazy evaluated descriptors
    # ---->
    @lazy_property
    def charge(self):
        setattr(Charge, '_api_client', self)
        return Charge

    @lazy_property
    def checkout(self):
        setattr(Checkout, '_api_client', self)
        return Checkout

    @lazy_property
    def event(self):
        setattr(Event, '_api_client', self)
        return Event
    # <----

    def _build_session(self, auth_class, *args, **kwargs):
        auth = auth_class(*args, **kwargs)

        headers = dict(self.DEFAULT_HEADERS)
        if isinstance(auth, APIAuthHeadersMixin):
            headers.update(auth.headers)

        return ClientSession(headers=headers)

    async def _request(self, method, *relative_path_parts, **kwargs):
        uri = self._create_api_uri(*relative_path_parts)
        data = kwargs.pop('data', None)

        if data and isinstance(data, dict):
            kwargs['data'] = encode_params(data)

        try:
            async with self.session.request(method, uri, **kwargs) as response:
                proceeded_response = await self._proceed_response(response)
        except Exception as e:
            self._handle_request_error(e)
        else:
            return proceeded_response

    async def _proceed_response(self, response):
        body = await response.read()
        try:
            response.raise_for_status()
        except ClientResponseError as err:
            raise _build_api_error(body=body,
                                   code=err.status,
                                   headers=err.headers)
        else:
            return CoinbaseResponse(body=body,
                                    code=response.status,
                                    headers=response.headers)

    async def close(self):
        await self.session.close()

    def __enter__(self):
        raise TypeError("Use async with instead")

    def __exit__(self, exc_type, exc_val, exc_tb):
        # __exit__ should exist in pair with __enter__ but never executed
        pass  # pragma: no cover

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
