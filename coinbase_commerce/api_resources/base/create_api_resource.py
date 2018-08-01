from coinbase_commerce import util
from coinbase_commerce.api_resources.base import APIResource


class CreateAPIResource(APIResource):
    """
    Create operations mixin
    """

    @classmethod
    def create(cls, **params):
        response = cls._api_client.post(cls.RESOURCE_PATH, data=params)
        return util.convert_to_api_object(response, cls._api_client, cls)
