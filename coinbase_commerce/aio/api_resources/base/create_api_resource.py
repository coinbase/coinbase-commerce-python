from coinbase_commerce import util
from . import APIResource

__all__ = (
    'CreateAPIResource',
)


class CreateAPIResource(APIResource):
    """
    Create operations mixin
    """

    @classmethod
    async def create(cls, **params):
        response = await cls._api_client.post(cls.RESOURCE_PATH, data=params)
        return util.convert_to_api_object(response, cls._api_client, cls)
