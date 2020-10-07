import humps
from qr_code.qrcode.maker import make_embedded_qr_code
from qr_code.qrcode.utils import QRCodeOptions

class Protocol:
    @property
    def protocol_ident(self):
        return f"{humps.decamelize(self._meta.model_name)}:{self.pk}"
    
    @property
    def protocol_self(self):
        return f"invo:{self.protocol_ident}"

    def qr(self, options=QRCodeOptions(error_correction="Q")):
        return make_embedded_qr_code(self.protocol_self, qr_code_options=options)