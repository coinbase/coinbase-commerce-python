from requests.auth import AuthBase
from requests.utils import to_native_string


class APIAuthHeadersMixin:
    api_key = None
    api_version = None

    @property
    def headers(self):
        return {
            to_native_string('X-CC-Version'): self.api_version,
            to_native_string('X-CC-Api-Key'): self.api_key,
        }


class APIAuth(APIAuthHeadersMixin, AuthBase):
    def __init__(self, api_key, api_version):
        self.api_key = api_key
        self.api_version = api_version

    def __call__(self, request):
        request.headers.update(self.headers)
        return request
