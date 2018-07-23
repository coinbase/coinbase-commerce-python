from coinbase_commerce.api_resources.base import CreateAPIResource
from coinbase_commerce.api_resources.base import DeleteAPIResource
from coinbase_commerce.api_resources.base import ListAPIResource
from coinbase_commerce.api_resources.base import UpdateAPIResource


class Checkout(ListAPIResource,
               CreateAPIResource,
               UpdateAPIResource,
               DeleteAPIResource):
    RESOURCE_PATH = "checkouts"
    RESOURCE_NAME = "checkout"
