import json

import six

from coinbase_commerce import util


class APIObject(dict):
    """
    Generic class used to represent a JSON response from the Coinbase API.
    """

    def __init__(self, api_client=None, data=None):
        super(APIObject, self).__init__()
        data = data or {}
        self._api_client = getattr(self, '_api_client', api_client)
        self._unsaved_values = set()
        self._passing_values = set()
        self.refresh_from(**data)

    def refresh_from(self, **kwargs):
        # update fields with new data if any
        removed = set(self.keys()) - set(kwargs)
        self._passing_values = self._passing_values | removed
        self._unsaved_values = set()
        self.clear()
        self._passing_values = self._passing_values - set(kwargs)
        # perform conversion for nested data
        for k, v in kwargs.items():
            converted_value = util.convert_to_api_object(v, api_client=self._api_client)
            super(APIObject, self).__setitem__(k, converted_value)

    def serialize(self):
        params = {}
        unsaved_keys = self._unsaved_values or set()

        for k, v in six.iteritems(self):
            if k == 'id' or (isinstance(k, str) and k.startswith('_')):
                continue
            elif hasattr(v, 'serialize'):
                if v.serialize():
                    params[k] = v
            elif k in unsaved_keys:
                params[k] = v

        return params

    def update(self, mapping, **kwargs):
        for k in mapping:
            self._unsaved_values.add(k)
        return super(APIObject, self).update(mapping, **kwargs)

    # do not include private and protected fields into json serialization
    def __setitem__(self, k, v):
        if not hasattr(self, '_unsaved_values'):
            self._unsaved_values = set()
        self._unsaved_values.add(k)
        super(APIObject, self).__setitem__(k, v)

    def __setattr__(self, k, v):
        if k[0] == '_' or k in self.__dict__:
            return super(APIObject, self).__setattr__(k, v)
        self[k] = v
        return None

    def __getattr__(self, k):
        if k[0] == '_':
            raise AttributeError(k)
        try:
            return self[k]
        except KeyError as err:
            raise AttributeError(*err.args)

    def __delattr__(self, k):
        if k[0] == '_' or k in self.__dict__:
            return super(APIObject, self).__delattr__(k)
        else:
            del self[k]

    def __delitem__(self, k):
        super(APIObject, self).__delitem__(k)
        if hasattr(self, '_unsaved_values'):
            self._unsaved_values.remove(k)

    def __str__(self):
        try:
            return json.dumps(self, sort_keys=True, indent=2)
        except TypeError:
            return '(invalid JSON)'

    def __repr__(self):
        return '<{} id={}> Serialized: {}'.format(type(self).__name__,
                                                  self.get('id', 'No ID'),
                                                  str(self))
