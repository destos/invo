import pytest
from model_bakery import baker

from protocol.models import IRN
from items.models import Item


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
    # with positional args
    irn = IRN.build("items.item", "456")
    assert str(irn) == "irn:test:items.item:456"

    # with kwargs
    irn = IRN.build(nss="456", etype="items.item")
    assert str(irn) == "irn:test:items.item:456"


def test_get_model():
    irn = IRN.build("items.item", "456")
    model = irn.get_model()
    assert model == Item


@pytest.mark.django_db()
def test_get_instance():
    item = baker.make("items.Item", id=456)
    irn = IRN.build("items.item", "456")
    instance = irn.get_instance()
    assert instance == item
