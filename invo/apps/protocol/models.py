import humps
from qr_code.qrcode.maker import make_embedded_qr_code
from qr_code.qrcode.utils import QRCodeOptions


class Protocol:
    @property
    def protocol_ident(self):
        # Only works on polymorphic models RN?
        label = self.get_real_concrete_instance_class()._meta.label_lower
        return f"{label}:{self.pk}"

    @property
    def protocol_self(self):
        return f"invo:{self.protocol_ident}"

    def qr(self, options=QRCodeOptions(error_correction="Q")):
        return make_embedded_qr_code(self.protocol_self, qr_code_options=options)
