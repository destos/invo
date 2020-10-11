from django.test import TestCase
from model_bakery import baker
import mock
# from mock import Mock

from . import models


class TestSpaceNode(TestCase):
    def setUp(self):
        self.space = baker.make(models.GridSpaceNode)

    # def test_attribues(self):
    #     meta = models.GridSpaceNode

    @mock.patch("spaces.models.SpaceNode.items")
    def xtest_item_count(self, mock_items):
        # import ipdb; ipdb.set_trace()
        # mocker.patch(self.space.items, return_value=mocker.Mock)
        # in_space_mock = mock_items.model.objects.in_space.return_value = Mock()
        # in_space_mock.count.return_value = 12

        mock_items.model.objects.in_space.count.return_value = 12

        self.assertEqual(self.space.item_count, 12)

        mock_items.model.objects.in_space.assert_called_with(self.space)
        in_space_mock.count.assert_called()

        # self.assertEqual(self.space.item_count, 0)
        # baker.make("items.Item", space=self.space)
        # import ipdb; ipdb.set_trace()
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


class TestGridSpaceNode(TestCase):
    def setUp(self):
        self.grid = baker.make(models.GridSpaceNode, grid_size=[4, 4])

    def test_grid_space_node_sync_children(self):
        self.assertEqual(self.grid.children.count(), 0)
        self.grid.sync_children()
        children = self.grid.children.all()
        self.assertEqual(children.count(), 16)
        self.assertIsInstance(children.last(), models.GridSpaceNode)
        self.assertEqual(children[0].name, "0,0")
        self.assertEqual(children[15].name, "3,3")

    def test_grid_space_node_sync_children_different_node(self):
        self.grid.sync_children(child_class=models.SpaceNode)
        children = self.grid.children
        self.assertEqual(children.last()._meta.model, models.SpaceNode)
        self.assertEqual(children.count(), 16)
