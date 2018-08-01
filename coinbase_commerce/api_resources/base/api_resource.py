from coinbase_commerce import util
from coinbase_commerce.api_resources.base import APIObject


class APIResource(APIObject):
    """
    Base API Resource class
    """

    @classmethod
    def retrieve(cls, entity_id, **params):
        response = cls._api_client.get(cls.RESOURCE_PATH, entity_id, params=params)
        api_obj = util.convert_to_api_object(response, cls._api_client, cls)
        return api_obj

    def refresh(self):
        entity_id = self.pop('id', None)
        if not entity_id:
            raise ValueError("Can't refresh {} without id. "
                             "Create or retrieve it first".format(self.__class__.__name__))
        response = self._api_client.get(self.RESOURCE_PATH, entity_id)
        data = util.convert_to_api_object(response, self._api_client, self.__class__)
        self.refresh_from(**data)
        return self

    @classmethod
    def get_subclasses(cls):
        for subclass in cls.__subclasses__():
            # py2 compatible kind of yield from
            for child_klass in subclass.get_subclasses():
                yield child_klass
            yield subclass
