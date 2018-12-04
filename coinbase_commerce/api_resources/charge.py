from coinbase_commerce.api_resources.base import CreateAPIResource
from coinbase_commerce.api_resources.base import ListAPIResource
from coinbase_commerce import util


@util.register_resource_cls
class Charge(ListAPIResource,
             CreateAPIResource):
    RESOURCE_PATH = "charges"
    RESOURCE_NAME = "charge"

    @classmethod
    def cancel(cls, entity_id, **params):
        response = cls._api_client.post(
            cls.RESOURCE_PATH, entity_id, 'cancel',
            data=params
        )
        api_obj = util.convert_to_api_object(response, cls._api_client, cls)
        return api_obj

    @classmethod
    def resolve(cls, entity_id, **params):
        response = cls._api_client.post(
            cls.RESOURCE_PATH, entity_id, 'resolve',
            data=params
        )
        api_obj = util.convert_to_api_object(response, cls._api_client, cls)
        return api_obj
