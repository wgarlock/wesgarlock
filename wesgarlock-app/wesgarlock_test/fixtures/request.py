from io import BytesIO

from django.core.serializers.json import DjangoJSONEncoder
from django.http import SimpleCookie
from django.test import RequestFactory


class HostNameRequestFactory(RequestFactory):
    def __init__(self, host_name, *, json_encoder=DjangoJSONEncoder, **defaults):
        self.host_name = host_name
        self.json_encoder = json_encoder
        self.defaults = defaults
        self.cookies = SimpleCookie()
        self.errors = BytesIO()

    def _base_environ(self, **request):
        env = super()._base_environ()
        env["SERVER_NAME"] = self.host_name
        return env
