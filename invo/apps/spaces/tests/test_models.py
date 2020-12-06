from django.test import TestCase
from model_bakery import baker
import mock

# from mock import Mock

from spaces import models


class TestSpaceNode(TestCase):
    def setUp(self):
        self.space = baker.make(models.GridSpaceNode)

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
        # baker.make("items.Item", space=self.space)
        # # self.space.refresh_from_db()
        # # models.SpaceNode.objects.rebuild()

        # # Other space items don't count
        # other_space = baker.make(models.GridSpaceNode)
        # baker.make("items.Item", space=other_space)

        # self.space.refresh_from_db()
        # self.assertEqual(self.space.item_count, 1)

        # # Spaces that exist under the original space do count
        # under_space = baker.make(models.GridSpaceNode, parent=self.space)
        # baker.make("items.Item", space=under_space)
        # # models.SpaceNode.objects.rebuild()
        # # self.space.refresh_from_db()
        # self.assertEqual(self.space.item_count, 2)

    def test_layout_property(self):
        # Default layout value is stored as None
        self.assertEqual(self.space.data, dict(layout=None))
        # Default layout values
        self.assertEqual(self.space._default_layout, dict(x=0, y=0, w=10, h=10))
        # The unset value of layout should use these values
        self.assertEqual(self.space.layout, dict(x=0, y=0, w=10, h=10))

        # Setting a value should merge it
        setattr(self.space, "layout", dict(w=100))
        self.assertEqual(self.space.layout, dict(x=0, y=0, w=100, h=10))

        # should also set the layout in the json data
        self.assertEqual(self.space.data["layout"], dict(x=0, y=0, w=100, h=10))

        self.space.save()

        # Values should persist after a save
        self.assertEqual(self.space.layout, dict(x=0, y=0, w=100, h=10))
        self.assertEqual(self.space.data["layout"], dict(x=0, y=0, w=100, h=10))


class TestGridSpaceNode(TestCase):
    def setUp(self):
        self.grid = baker.make(models.GridSpaceNode, grid_size=[4, 4])

    def test_sync_children(self):
        self.assertEqual(self.grid.children.count(), 0)
        self.grid.sync_children()
        children = self.grid.children.all()
        self.assertEqual(children.count(), 16)
        self.assertIsInstance(children.last(), models.SpaceNode)
        self.assertEqual(children[0].name, "0,0")
        self.assertEqual(children[15].name, "3,3")

    def test_sync_children_different_node(self):
        "Use a different child class than the default SpaceNode"
        self.grid.sync_children(child_class=models.GridSpaceNode)
        children = self.grid.children.all()
        self.assertTrue(all([child._meta.model == models.GridSpaceNode for child in children]))
        self.assertEqual(children.count(), 16)

    def test_sync_children_existing_nodes(self):
        "Existing nodes with a proper position shouldn't be replaced or removed"
        baker.make(models.SpaceNode, parent=self.grid, data=dict(position=[0, 0]))
        self.grid.sync_children(child_class=models.GridSpaceNode)
        children = self.grid.children.instance_of(models.GridSpaceNode)
        orig_children = self.grid.children.instance_of(models.SpaceNode)
        self.assertTrue(all([child._meta.model == models.GridSpaceNode for child in children]))
        self.assertEqual(children.count(), 15)
        self.assertEqual(orig_children.count(), 16)

    def test_sync_children_removing_nodes(self):
        "When the size of a grid changes to reduce the grid size, spaces are deleted"
        self.grid.sync_children()
        children = self.grid.children.all()
        self.assertEqual(children.count(), 16)

        self.grid.grid_size = [2, 2]

        self.grid.sync_children()
        children = self.grid.children.all()
        self.assertEqual(children.count(), 4)
        self.assertEqual(models.SpaceNode.deleted_objects.count(), 12)

    def test_sync_children_reusing_removed_nodes(self):
        "When the size of a grid changes to reduce the grid size, spaces are deleted"
        self.grid.sync_children()
        children = self.grid.children.all()
        self.assertEqual(children.count(), 16)

        # Undersize grid, removes many nodes
        self.grid.grid_size = [2, 2]

        self.grid.sync_children()
        children = self.grid.children.all()
        self.assertEqual(children.count(), 4)
        self.assertEqual(models.SpaceNode.deleted_objects.count(), 12)

        # Add two more x grid spaces
        self.grid.grid_size = [4, 2]

        self.grid.sync_children()
        children = self.grid.children.all()
        self.assertEqual(children.count(), 8)
        self.assertEqual(models.SpaceNode.deleted_objects.count(), 8)

    # def test_generate_grid(self):
