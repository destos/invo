from django.test import TestCase
from model_bakery import baker
from . import models


class TestGridSpaceNode(TestCase):
    def setUp(self):
        self.grid = baker.make("spaces.GridSpaceNode", grid_size=[4, 4])

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
