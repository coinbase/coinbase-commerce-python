from collections import deque

from coinbase_commerce import util
from . import APIResource

__all__ = (
    'ListAPIResource',
)


class ListAPIResource(APIResource):
    """
    List operations mixin
    """

    @classmethod
    async def list(cls, **params):
        response = await cls._api_client.get(cls.RESOURCE_PATH, params=params)
        return util.convert_to_api_object(
            response=response,
            api_client=cls._api_client,
            resource_class=cls
        )

    @classmethod
    def list_paging_iter(cls, **params):
        return _PagingIter(cls.list, **params)


class _PagingIter:
    __slots__ = (
        '_coro',
        '_params',
        '_items',
    )

    def __init__(self, coro, **params):
        self._coro = coro
        self._params = params
        self._items = deque()

    async def __aiter__(self):
        return self

    def _is_empty(self):
        return not self._items

    def _extend(self, data):
        self._items.extendleft(data)

    def _pop(self):
        try:
            return self._items.pop()
        except IndexError:
            raise StopAsyncIteration from None

    async def __anext__(self):
        if not self._is_empty():
            return self._pop()

        page = await self._coro(**self._params)
        data = page.get('data', [])
        pagination = page.get('pagination', {})
        shown = pagination.get('yielded', 0)
        limit = pagination.get('limit', 0)
        cursor_range = pagination.get('cursor_range', [])
        self._extend(data)

        if shown < limit and self._is_empty():
            raise StopAsyncIteration

        if isinstance(cursor_range, list) and cursor_range:
            self._params['starting_after'] = cursor_range[-1]
        else:
            raise StopAsyncIteration

        return self._pop()
