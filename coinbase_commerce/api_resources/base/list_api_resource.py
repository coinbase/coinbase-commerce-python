from coinbase_commerce import util
from coinbase_commerce.api_resources.base import APIResource


class ListAPIResource(APIResource):
    """
    List operations mixin
    """

    @classmethod
    def list(cls, **params):
        response = cls._api_client.get(cls.RESOURCE_PATH, params=params)
        return util.convert_to_api_object(response, api_client=cls._api_client, resource_class=cls)

    @classmethod
    def list_paging_iter(cls, **params):
        while True:
            page = cls.list(**params)
            data = page.get('data', [])
            pagination = page.get('pagination', {})
            shown = pagination.get('yielded', 0)
            limit = pagination.get('limit', 0)
            cursor_range = pagination.get('cursor_range', [])

            for item in data:
                yield item

            if shown < limit:
                return

            if isinstance(cursor_range, list) and cursor_range:
                params['starting_after'] = cursor_range[-1]
            else:
                return
