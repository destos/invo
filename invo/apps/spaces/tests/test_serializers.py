import pytest
from measurement.measures import Distance
from model_bakery import baker
from spaces.models import GridSpaceNode, SpaceNode
from spaces.serializers import GridSpaceNodeSerializer, SpaceNodeSerializer


@pytest.mark.django_db()
def test_space_serializer_success():
    space = baker.make(SpaceNode)
    SpaceNode.objects.rebuild()
    ser = SpaceNodeSerializer(
        space,
        data=dict(
            dimensions=dict(x=Distance(m=2), y=Distance(m=2), z=Distance(m=4)),
            name="bob",
            # layout=dict(x=10, y=12, w=3, h=5),
        ),
    )
    valid = ser.is_valid()
    assert ser.errors == dict()
    assert valid == True
    ser.save()
    assert space.size == [Distance(m=2), Distance(m=2), Distance(m=4)]
    # assert space.layout == dict(x=10, y=12, w=3, h=5)


@pytest.mark.django_db()
def test_grid_serializer_success():
    space = baker.make(GridSpaceNode)
    GridSpaceNode.objects.rebuild()
    ser = GridSpaceNodeSerializer(
        space,
        data=dict(
            dimensions=dict(x=Distance(m=2), y=Distance(m=2), z=Distance(m=4)),
            size=dict(cols=4, rows=2),
            name="bob",
            # layout=dict(x=10, y=12, w=3, h=5),
        ),
    )
    valid = ser.is_valid()
    assert ser.errors == dict()
    assert valid == True
    ser.save()
    assert space.grid_size == [4, 2]
