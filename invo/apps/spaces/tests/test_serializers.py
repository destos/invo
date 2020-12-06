import pytest
from measurement.measures import Distance
from model_bakery import baker
from spaces.models import SpaceNode
from spaces.serializers import SpaceNodeSerializer


@pytest.mark.django_db()
def test_serializer_success():
    space = baker.make(SpaceNode)
    SpaceNode.objects.rebuild()
    ser = SpaceNodeSerializer(
        space,
        data=dict(dimensions=dict(x=Distance(m=2), y=Distance(m=2), z=Distance(m=4)), name="bob"),
    )
    valid = ser.is_valid()
    assert valid == True
    assert ser.errors == dict()
    ser.save()
    assert space.size == [Distance(m=2), Distance(m=2), Distance(m=4)]
