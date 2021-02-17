from decimal import Decimal

import mock
import pytest
from django.contrib.sites.models import Site
from django.test import TestCase
from measurement.measures import Distance
from model_bakery import baker
from spaces import models


def test_layout_apply_delta():
    layout = models.Layout(0, 1, 2, 4)

    new_layout = layout * 2
    assert new_layout == models.Layout(0, 2, 4, 8)


def test_layout_invalid_delta():
    layout = models.Layout(0, 1, 2, 4)

    with pytest.raises(TypeError):
        layout * 0.5


class TestSpaceNode(TestCase):
    def setUp(self):
        self.site = Site.objects.get()
        self.space = baker.make(models.SpaceNode, site=self.site)

    # def test_attribues(self):
    #     meta = models.GridSpaceNode

    @mock.patch("spaces.models.SpaceNode.items")
    def xtest_item_count(self, mock_items):
        # mocker.patch(self.space.items, return_value=mocker.Mock)
        # in_space_mock = mock_items.model.objects.in_space.return_value = Mock()
        # in_space_mock.count.return_value = 12

        mock_items.model.objects.in_space.count.return_value = 12

        self.assertEqual(self.space.item_count, 12)

        mock_items.model.objects.in_space.assert_called_with(self.space)
        in_space_mock.count.assert_called()

        # self.assertEqual(self.space.item_count, 0)
        # baker.make("items.Item", space=self.space, site=self.site)
        # # self.space.refresh_from_db()
        # # models.SpaceNode.objects.rebuild()

        # # Other space items don't count
        # other_space = baker.make(models.GridSpaceNode, site=self.site)
        # baker.make("items.Item", space=other_space, site=self.site)

        # self.space.refresh_from_db()
        # self.assertEqual(self.space.item_count, 1)

        # # Spaces that exist under the original space do count
        # under_space = baker.make(models.GridSpaceNode, parent=self.space, site=self.site)
        # baker.make("items.Item", space=under_space, site=self.site)
        # # models.SpaceNode.objects.rebuild()
        # # self.space.refresh_from_db()
        # self.assertEqual(self.space.item_count, 2)

    def test_layout_property(self):
        # Default layout value is stored as None
        self.assertEqual(self.space.data, dict())
        # Default layout values
        self.assertEqual(self.space._default_layout, dict(x=0, y=0, w=10, h=10))
        # The unset value of layout should use these values
        self.assertEqual(self.space.layout, models.Layout(0, 0, 10, 10))

        # Setting a value should merge it
        self.space.layout = dict(w=100)
        self.assertEqual(self.space.layout, models.Layout(0, 0, 100, 10))

        # should also set the layout in the json data
        self.assertEqual(self.space.data["layout"], dict(x=0, y=0, w=100, h=10))

        self.space.save()

        # Values should persist after a save
        self.assertEqual(self.space.layout, models.Layout(0, 0, 100, 10))
        self.assertEqual(self.space.data["layout"], dict(x=0, y=0, w=100, h=10))

    def test_update_data(self):
        # can just pass one item to add
        self.space.update_data(master=True)
        self.assertEqual(self.space.data, dict(master=True))

        # can provide defaults to update values
        self.space.update_data(
            something="okay", defaults=dict(something="earlier", another="thing")
        )
        self.assertEqual(self.space.data, dict(something="okay", another="thing", master=True))
        # TODO: nested values

    # def test_space_grid_config(self):
    #     pass

    def test_space_grid_config(self):
        self.space.size = [Distance("1 m"), Distance("80 cm"), Distance("20 cm")]
        self.space.grid_scale = Distance("1 cm")
        config = self.space.grid_config
        assert config == dict(cols=100, row_basis=Decimal("0.80"))

    def test_space_scale_change_adjusts_children_layout(self):
        # meter by meter front area, layout grid is half a meter
        self.space.size = [Distance("1 m"), Distance("1 m"), Distance("20 cm")]
        self.space.grid_scale = Distance("0.5 m")

        # Positioning of children, two in a top row
        child1 = baker.make(models.SpaceNode, parent=self.space, site=self.site)
        child1.layout = models.Layout(0, 0, 1, 1)

        child2 = baker.make(models.SpaceNode, parent=self.space, site=self.site)
        child2.layout = models.Layout(1, 0, 1, 1)

        # One that takes up the full bottom
        child3 = baker.make(models.SpaceNode, parent=self.space, site=self.site)
        child3.layout = models.Layout(0, 1, 2, 1)

        self.space.save()
        # layout of children should not change

        child1.refresh_from_db()
        assert child1.layout == models.Layout(0, 0, 1, 1)
        child2.refresh_from_db()
        assert child2.layout == models.Layout(1, 0, 1, 1)
        child3.refresh_from_db()
        assert child3.layout == models.Layout(0, 1, 2, 1)

        # Layout of children should double
        self.space.grid_scale = Distance(meter=0.25)
        self.space.save()

        child1.refresh_from_db()
        assert child1.layout == models.Layout(0, 0, 2, 2)
        child2.refresh_from_db()
        assert child2.layout == models.Layout(2, 0, 2, 2)
        child3.refresh_from_db()
        assert child3.layout == models.Layout(0, 2, 4, 2)

        # Layout of children should expand more
        self.space.grid_scale = Distance(cm=1)
        self.space.save()

        child1.refresh_from_db()
        assert child1.layout == models.Layout(0, 0, 50, 50)
        child2.refresh_from_db()
        assert child2.layout == models.Layout(50, 0, 50, 50)
        child3.refresh_from_db()
        assert child3.layout == models.Layout(0, 50, 100, 50)

        # TODO: If a layout becomes more specific when the scale gets larger,
        # handle sibling layout issues and prevent collapsing sibling layouts to unusable sizes.

    # def test_space_grid_basic_throws_if_not_divisible(self):
    #     pass

    # def test_grid_basis(self):
    #     self.space.size = [Distance("1 m"), Distance("80 cm"), Distance("20 cm")]
    #     self.space.grid_scale = Distance("1 cm")

    #     self.space.save()
    #     basis = self.space.grid_basis
    #     assert basis == 1


class TestGridSpaceNode(TestCase):
    def setUp(self):
        self.site = Site.objects.get()
        self.space = baker.make(models.GridSpaceNode, grid_size=[4, 4], site=self.site)

    def test_sync_children(self):
        self.assertEqual(self.space.children.count(), 0)
        self.space.sync_children()
        children = self.space.children.all()
        self.assertEqual(children.count(), 16)
        self.assertIsInstance(children.last(), models.SpaceNode)
        self.assertEqual(children[0].name, "0,0")
        self.assertEqual(children[15].name, "3,3")

    def test_sync_children_different_node(self):
        "Use a different child class than the default SpaceNode"
        self.space.sync_children(child_class=models.GridSpaceNode)
        children = self.space.children.all()
        self.assertTrue(all([child._meta.model == models.GridSpaceNode for child in children]))
        self.assertEqual(children.count(), 16)

    def test_sync_children_existing_nodes(self):
        "Existing nodes with a proper position shouldn't be replaced or removed"
        baker.make(
            models.SpaceNode,
            parent=self.space,
            data=dict(position=[0, 0]),
            site=self.site,
        )
        self.space.sync_children(child_class=models.GridSpaceNode)
        children = self.space.children.instance_of(models.GridSpaceNode)
        orig_children = self.space.children.instance_of(models.SpaceNode)
        self.assertTrue(all([child._meta.model == models.GridSpaceNode for child in children]))
        self.assertEqual(children.count(), 15)
        self.assertEqual(orig_children.count(), 16)

    def test_sync_children_removing_nodes(self):
        "When the size of a grid changes to reduce the grid size, spaces are deleted"
        self.space.sync_children()
        children = self.space.children.all()
        self.assertEqual(children.count(), 16)

        self.space.grid_size = [2, 2]

        self.space.sync_children()
        children = self.space.children.all()
        self.assertEqual(children.count(), 4)
        self.assertEqual(models.SpaceNode.deleted_objects.count(), 12)

    def test_sync_children_reusing_removed_nodes(self):
        "When the size of a grid changes to reduce the grid size, spaces are deleted"
        self.space.sync_children()
        children = self.space.children.all()
        self.assertEqual(children.count(), 16)

        # Undersize grid, removes many nodes
        self.space.grid_size = [2, 2]

        self.space.sync_children()
        children = self.space.children.all()
        self.assertEqual(children.count(), 4)
        self.assertEqual(models.SpaceNode.deleted_objects.count(), 12)

        # Add two more x grid spaces
        self.space.grid_size = [4, 2]

        self.space.sync_children()
        children = self.space.children.all()
        self.assertEqual(children.count(), 8)
        self.assertEqual(models.SpaceNode.deleted_objects.count(), 8)

    # def test_generate_grid(self):
