from coinbase_commerce.api_resources.base import ListAPIResource
from coinbase_commerce.util import register_resource_cls


@register_resource_cls
class Event(ListAPIResource):
    RESOURCE_PATH = "events"
    RESOURCE_NAME = "event"
