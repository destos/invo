import pytest
from model_bakery import baker

from ..conditions import (
    ItemsSelected,
    OnlyItemsSelected,
    OnlySpacesSelected,
    SelectedItemInSpace,
    SpaceSelected,
    TwoSpacesSelected,
    ItemsInSameSpace,
)


@pytest.mark.django_db()
def test_selected_item_in_space():
    situ = baker.make("situations.Situation")
    space = baker.make("spaces.SpaceNode")
    item = baker.make("items.Item")
    conditions = SelectedItemInSpace

    # No items in selected space
    situ.spaces.add(space)
    assert conditions().has_object_condition(situ, item) is False

    # Presense of an item sets tem in space true
    space.add_item(item)
    assert conditions().has_object_condition(situ, item) is True


# TODO: test select has_object_condition with things other than item


@pytest.mark.django_db()
def test_two_spaces_selected():
    situ = baker.make("situations.Situation")
    space = baker.make("spaces.SpaceNode")
    space2 = baker.make("spaces.SpaceNode")
    conditions = TwoSpacesSelected

    # No items in selected space
    situ.spaces.add(space)
    assert conditions().has_condition(situ) is False

    # Presense of an item sets tem in space true
    situ.spaces.add(space2)
    assert conditions().has_condition(situ) is True


@pytest.mark.django_db()
def test_only_spaces_selected():
    situ = baker.make("situations.Situation")
    space = baker.make("spaces.SpaceNode")
    space2 = baker.make("spaces.SpaceNode")
    item = baker.make("items.Item")
    conditions = OnlySpacesSelected

    # one space selected
    situ.spaces.add(space)
    assert conditions().has_condition(situ) is True

    # two spaces
    situ.spaces.add(space2)
    assert conditions().has_condition(situ) is True

    # adding item makes false
    situ.items.add(item)
    assert conditions().has_condition(situ) is False


@pytest.mark.django_db()
def test_only_items_selected():
    situ = baker.make("situations.Situation")
    space = baker.make("spaces.SpaceNode")
    item = baker.make("items.Item")
    item2 = baker.make("items.Item")
    conditions = OnlyItemsSelected

    # one item selected
    situ.items.add(item)
    assert conditions().has_condition(situ) is True

    # two items
    situ.items.add(item2)
    assert conditions().has_condition(situ) is True

    # adding space makes false
    situ.spaces.add(space)
    assert conditions().has_condition(situ) is False


@pytest.mark.django_db()
def test_space_selected():
    situ = baker.make("situations.Situation")
    space = baker.make("spaces.SpaceNode")
    conditions = SpaceSelected

    # No space selected
    assert conditions().has_condition(situ) is False

    # Presense of an space returns True
    situ.spaces.add(space)
    assert conditions().has_condition(situ) is True


@pytest.mark.django_db()
def test_item_selected():
    situ = baker.make("situations.Situation")
    item = baker.make("items.Item")
    conditions = ItemsSelected

    # No item selected
    assert conditions().has_condition(situ) is False

    # Presense of an item returns True
    situ.items.add(item)
    assert conditions().has_condition(situ) is True


@pytest.mark.django_db()
def test_items_in_same_space():
    situ = baker.make("situations.Situation")
    space = baker.make("spaces.SpaceNode")
    space2 = baker.make("spaces.SpaceNode")
    item = baker.make("items.Item", space=space)
    item2 = baker.make("items.Item", space=space)
    item3 = baker.make("items.Item", space=space2)
    conditions = ItemsInSameSpace

    # first two items are in the same space
    situ.items.add(item)
    situ.items.add(item2)
    assert conditions().has_condition(situ) is True

    # last space is not in the same space
    situ.items.add(item3)
    assert conditions().has_condition(situ) is False
