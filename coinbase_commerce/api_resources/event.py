from coinbase_commerce.api_resources.base import ListAPIResource


class Event(ListAPIResource):
    RESOURCE_PATH = "events"
    RESOURCE_NAME = "event"
