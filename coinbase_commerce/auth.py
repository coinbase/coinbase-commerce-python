from requests.auth import AuthBase
from requests.utils import to_native_string


class APIAuth(AuthBase):
    def __init__(self, api_key, api_version):
        self.api_key = api_key
        self.api_version = api_version

    def __call__(self, request):
        request.headers.update({
            to_native_string('X-CC-Version'): self.api_version,
            to_native_string('X-CC-Api-Key'): self.api_key,
        })
        return request
