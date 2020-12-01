from typing import NamedTuple, Union
from base64 import b64encode

import humps
# from qr_code.qrcode.maker import make_qr
# from qr_code.qrcode.utils import QRCodeOptions
import segno
from django.apps import apps
from django.conf import settings


class UrnNamespaceRegistrar:
    _models = dict()

    @classmethod
    def register(cls, model):
        pass


class IRN(NamedTuple):
    """
    Invo Resource Name
    Custom URN protocol for referencing entities in our system
    https://en.wikipedia.org/wiki/Uniform_Resource_Name

    "irn:<app_namespace>:<entity_identifier_nid:<nss>"
    """

    # TODO: namespace instance validation

    name: str = "irn"
    instance: str = ""  # invo app namespace (instance), distinguish app instance, can be blank
    etype: str = ""  # entity type, used for lookup
    nss: Union[int, str] = None  # entity PK, used for lookup

    @classmethod
    def parse(cls, urn: str):
        args = urn.split(":")
        return cls(*args)

    @classmethod
    def build(cls, *args, **kwargs):
        instance = getattr(settings, "INVO_APP_IRN_NAMESPACE", None)
        return cls("irn", instance, *args, **kwargs)

    def __str__(self):
        return ":".join([str(v) for v in self._asdict().values()])

    def get_model(self):
        return apps.get_model(self.etype)

    def get_instance(self):
        return self.get_model().objects.get(id=self.nss)


class Protocol:
    # TODO: model setup/init assert that used on polymorphic model or the ident

    # @property
    # def urn_nid(self):
    #     """The urn invo namespace id, identifies the type of entity we're working with"""

    # TODO: memoize per model type?
    @property
    def urn_etype(self):
        # Only works on polymorphic models right now
        return self.get_real_concrete_instance_class()._meta.label_lower

    @property
    def urn(self):
        return IRN.build(etype=self.urn_etype, nss=self.pk)

    @property
    def irn(self):
        return str(self.urn)

    def make_qr(self):
        return segno.make(self.irn, error="H")

    # TODO: memoize
    @property
    def qr(self):
        qr = self.make_qr()
        return qr.svg_data_uri()
