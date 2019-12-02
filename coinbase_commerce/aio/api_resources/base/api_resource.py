from coinbase_commerce import util
from coinbase_commerce.api_resources.base import APIResource as SyncAPIResource

__all__ = (
    'APIResource',
)


class APIResource(SyncAPIResource):
    """
    Base Async API Resource class
    """

    @classmethod
    async def retrieve(cls, entity_id, **params):
        response = await cls._api_client.get(
            cls.RESOURCE_PATH, entity_id,
            params=params
        )
        api_obj = util.convert_to_api_object(response, cls._api_client, cls)
        return api_obj

    async def refresh(self):
        entity_id = self.pop('id', None)
        if not entity_id:
            raise ValueError(
                "Can't refresh {} without id. "
                "Create or retrieve it first".format(self.__class__.__name__)
            )
        response = await self._api_client.get(self.RESOURCE_PATH, entity_id)
        data = util.convert_to_api_object(
            response=response,
            api_client=self._api_client,
            resource_class=self.__class__
        )
        self.refresh_from(**data)
        return self
