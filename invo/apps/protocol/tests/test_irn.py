from protocol.models import IRN


def test_irn_class():
    # Default named tuple usage
    irn = IRN("irn", "test", "items.item", "456")

    assert str(irn) == "irn:test:items.item:456"


def test_irn_parse():
    # parse class helper
    irn = IRN.parse("irn:test:items.item:456")

    assert irn.name == "irn"
    assert irn.ins == "test"
    assert irn.etype == "items.item"
    assert irn.nss == "456"


def test_irn_build(settings):
    # build class helper
    settings.INVO_APP_IRN_NAMESPACE = "test"

    # with positional args
    irn = IRN.build("items.item", "456")
    assert str(irn) == "irn:test:items.item:456"

    # with kwargs
    irn = IRN.build(nss="456", etype="items.item")
    assert str(irn) == "irn:test:items.item:456"
