from coinbase_commerce.api_resources.base import CreateAPIResource
from coinbase_commerce.api_resources.base import ListAPIResource
from coinbase_commerce import util


@util.register_resource_cls
class Charge(ListAPIResource,
             CreateAPIResource):
    RESOURCE_PATH = "charges"
    RESOURCE_NAME = "charge"
