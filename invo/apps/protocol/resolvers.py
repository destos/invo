from .types import protocol_interface


protocol_interface.set_field("protocolUri", lambda x, _: x.protocol_self)
