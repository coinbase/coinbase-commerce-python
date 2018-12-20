from coinbase_commerce.util import register_resource_cls
from .base import (
    CreateAPIResource,
    DeleteAPIResource,
    ListAPIResource,
    UpdateAPIResource,
)

__all__ = (
    'Checkout',
)


@register_resource_cls
class Checkout(ListAPIResource,
               CreateAPIResource,
               UpdateAPIResource,
               DeleteAPIResource):
    RESOURCE_PATH = "checkouts"
    RESOURCE_NAME = "checkout_aio"
