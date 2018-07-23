from coinbase_commerce.api_resources.base import CreateAPIResource
from coinbase_commerce.api_resources.base import ListAPIResource


class Charge(ListAPIResource,
             CreateAPIResource):
    RESOURCE_PATH = "charges"
    RESOURCE_NAME = "charge"
