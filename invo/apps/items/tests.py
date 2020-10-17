from django.test import TestCase
from model_bakery import baker
from . import models
from spaces.models import SpaceNode


class TestItemQueryset(TestCase):
    def setUp(self):
        # with SpaceNode.objects.delay_mptt_updates():
        self.top_space = baker.make(SpaceNode, name="Top Space")
        self.inner_space = baker.make(SpaceNode, name="Inner Space", parent=self.top_space)
        self.leaf_space = baker.make(SpaceNode, name="Leaf Space", parent=self.inner_space)
        # Empty space with no item inside
        baker.make(SpaceNode, name="Empty Space", parent=self.leaf_space)
        outside_space = baker.make(SpaceNode, name="Outside Space")

        # rebuild tree
        SpaceNode.objects.rebuild()
        self.top_space.refresh_from_db()
        self.inner_space.refresh_from_db()
        self.leaf_space.refresh_from_db()

        self.leaf_item = baker.make(models.Item, name="Leaf Item", space=self.leaf_space)
        self.inner_item = baker.make(models.Item, name="Inner Item", space=self.inner_space)
        self.top_item = baker.make(models.Item, name="Top Item", space=self.top_space)
        # These items shouldn't show up in our tests
        baker.make(models.Item, name="Extra Item")
        baker.make(models.Item, name="Outside Item", space=outside_space)

    def test_manager_in_space_items(self):
        self.assertSequenceEqual(
            models.Item.objects.in_space(self.top_space),
            [self.top_item, self.inner_item, self.leaf_item],
            "Should include all leafs",
        )
        self.assertSequenceEqual(
            models.Item.objects.in_space(self.inner_space),
            [self.inner_item, self.leaf_item],
            "Should include just inner items",
        )
        self.assertSequenceEqual(
            models.Item.objects.in_space(self.leaf_space),
            [self.leaf_item],
            "Should only be the leaf node",
        )


class TestItem(TestCase):
    def setUp(self):
        self.item = baker.make(models.Item, name="Test Item", data=dict(test="data"), id=21)

    def test_attrs(self):
        self.assertEqual(str(self.item), "Test Item")
        self.assertEqual(self.item.protocol_ident, "items.item:21")
        self.assertEqual(self.item.protocol_self, "invo:items.item:21")

    def test_item_can_be_assigned_to_space(self):
        node = baker.make(SpaceNode)
        self.item.space = node
        self.item.save()
        self.assertEqual(node.items.count(), 1)


class TestConsumable(TestCase):
    def setUp(self):
        self.item = baker.make(models.Consumable, name="Test Consumable", id=42)

    def test_attrs(self):
        self.assertEqual(str(self.item), "Test Consumable")
        self.assertEqual(self.item.protocol_ident, "items.consumable:42")
        self.assertEqual(self.item.protocol_self, "invo:items.consumable:42")

    def test_default_state(self):
        self.assertEqual(self.item.count, 0)
        self.assertEqual(self.item.warning_enabled, False)
        self.assertEqual(self.item.warning_count, 10)

    def test_warning(self):
        self.assertFalse(self.item.warning, "Warning should not be on by default")
        self.item.count = 20
        self.assertFalse(self.item.warning, "Warning should not be on by default with high count")

        self.item.warning_enabled = True
        self.assertFalse(self.item.warning, "warning shouldn't trigger with hight count")

        self.item.count = 10
        self.assertTrue(self.item.warning, "Warning is true when count is equal to warning")

        self.item.count = 5
        self.assertTrue(self.item.warning, "Warning is true warning count is below current count")

    def test_consume(self):
        self.item.count = 30
        first_modified = self.item.modified
        self.item.consume()
        self.assertEqual(self.item.count, 29)
        self.assertNotEqual(
            first_modified,
            self.item.modified,
            "my default consume should update modified date",
        )

        self.item.consume(20)
        self.assertEqual(self.item.count, 9)
        self.assertNotEqual(first_modified, self.item.modified)

    def test_addition(self):
        self.item.count = 10
        first_modified = self.item.modified
        self.item.addition()
        self.assertEqual(self.item.count, 11)
        self.assertNotEqual(
            first_modified,
            self.item.modified,
            "my default addition should update modified date",
        )

        self.item.addition(20)
        self.assertEqual(self.item.count, 31)
        self.assertNotEqual(first_modified, self.item.modified)


class TestTrackedConsumable(TestCase):
    def setUp(self):
        self.item = baker.make(models.TrackedConsumable, name="Test Tracked Consumable", id=84)

    def test_attrs(self):
        self.assertEqual(str(self.item), "Test Tracked Consumable")
        self.assertEqual(self.item.protocol_ident, "items.trackedconsumable:84")
        self.assertEqual(self.item.protocol_self, "invo:items.trackedconsumable:84")
