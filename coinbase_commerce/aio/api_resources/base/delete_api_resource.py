from coinbase_commerce import util
from . import APIResource

__all__ = (
    'DeleteAPIResource',
)


class DeleteAPIResource(APIResource):
    """
    Delete operations mixin
    """

    async def delete(self, **params):
        entity_id = self.get('id')
        if not entity_id:
            raise ValueError(
                "Can't delete {} without id. "
                "Create or retrieve it first".format(self.__class__.__name__)
            )
        response = await self._api_client.delete(
            self.RESOURCE_PATH, entity_id,
            data=params
        )
        data = util.convert_to_api_object(
            response=response,
            api_client=self._api_client,
            resource_class=self.__class__
        )
        self.refresh_from(**data)
        return self
