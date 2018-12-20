from coinbase_commerce import util
from . import APIResource

__all__ = (
    'UpdateAPIResource',
)


class UpdateAPIResource(APIResource):
    """
    Update operations mixin
    """

    @classmethod
    async def modify(cls, entity_id, **params):
        response = await cls._api_client.put(
            cls.RESOURCE_PATH, entity_id,
            data=params
        )
        return util.convert_to_api_object(response, cls._api_client, cls)

    async def save(self):
        entity_id = self.pop('id', None)
        if not entity_id:
            raise ValueError(
                "Can't update {} without id. "
                "Create or retrieve it first".format(self.__class__.__name__)
            )
        response = await self._api_client.put(
            self.RESOURCE_PATH, entity_id,
            data=self.serialize()
        )
        data = util.convert_to_api_object(
            response=response,
            api_client=self._api_client,
            resource_class=self.__class__
        )
        self.refresh_from(**data)
        return self
