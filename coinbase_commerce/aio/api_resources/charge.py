from coinbase_commerce import util
from .base import CreateAPIResource, ListAPIResource

__all__ = (
    'Charge',
)


@util.register_resource_cls
class Charge(ListAPIResource, CreateAPIResource):
    RESOURCE_PATH = "charges"
    RESOURCE_NAME = "charge_aio"

    @classmethod
    async def cancel(cls, entity_id, **params):
        response = await cls._api_client.post(
            cls.RESOURCE_PATH, entity_id, 'cancel',
            data=params
        )
        return util.convert_to_api_object(response, cls._api_client, cls)

    @classmethod
    async def resolve(cls, entity_id, **params):
        response = await cls._api_client.post(
            cls.RESOURCE_PATH, entity_id, 'resolve',
            data=params
        )
        return util.convert_to_api_object(response, cls._api_client, cls)
