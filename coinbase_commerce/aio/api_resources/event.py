from coinbase_commerce.util import register_resource_cls
from .base import ListAPIResource

__all__ = (
    'Event',
)


@register_resource_cls
class Event(ListAPIResource):
    RESOURCE_PATH = "events"
    RESOURCE_NAME = "event_aio"
