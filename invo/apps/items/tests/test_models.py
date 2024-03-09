from unittest.mock import patch

from django.test import TestCase
from marshmallow import fields
from model_bakery import baker

from items import models
from items.models import Declaration
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
        self.assertEqual(self.item.urn_etype, "items.item")
        self.assertEqual(self.item.irn, "irn:test:items.item:21")

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
        self.assertEqual(self.item.urn_etype, "items.consumable")
        self.assertEqual(self.item.irn, "irn:test:items.consumable:42")

    def test_default_state(self):
        self.assertEqual(self.item.count, 0)
        self.assertEqual(self.item.warning_enabled, False)
        self.assertEqual(self.item.warning_count, 1)

    def test_warning(self):
        self.item.warning_count = 10
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
        self.assertEqual(self.item.urn_etype, "items.trackedconsumable")
        self.assertEqual(self.item.irn, "irn:test:items.trackedconsumable:84")


class TestItemVariant(TestCase):
    def setUp(self):
        self.variant = baker.make("Variant", label="A bit", name="bit", options=[])

    def xtest_attrs(self):
        self.assertEqual(self.variant.name, "bit")
        self.assertEqual(self.variant.label, "A bit")


class TestItemDeclaration(TestCase):
    """
    A screw

    metric screw
    standards
    pitch 0.2 to 6
    calculated variation as a combination of multiple variations?

    Should there be a form of layering where you can apply the declaration and then make variant modifications?
    say we

    When adding a new declaration variant, you can add more variants and they are added to to the variants as potentially outliers?
    """

    maxDiff = None

    def setUp(self):
        self.declaration = baker.make(Declaration, name="Metric screws")
        self.declaration.add_variant("Diameter", "dia", "1", "2", "3", "4", "5")
        self.declaration.add_variant("Length", "length", "1", "2", "3")
        self.declaration.add_variant(
            "Pitch",
            "pitch",
            "0.2",
            "0.25",
            "0.3",
            "0.35",
            "0.4",
            "0.5",
            "1",
            # TODO: conditions are applied to a variant schema def to validate it in comparison to other
            # variants or data
            conditions=dict(),
        )
        # self.m3 = baker.make("Configuration", dia=3, pitch=0.5)
        # self.declaration.add_variant()

    # TODO: create configuration from options

    def xtest_attrs(self):
        self.assertEqual(self.declaration.name, "Metric screws")

    @patch("items.models.Schema")
    def xtest_schema_generation(self, mock_Schema):
        # Generate schema
        result = self.declaration.schema

        # self.assertEqual(result, mock_Schema.from_dict)

        mock_Schema.from_dict.assert_called()
        from_dict_arg = mock_Schema.from_dict.call_args.args[0]
        self.assertDictEqual(
            from_dict_arg, dict(dia=fields.Str(), length=fields.Str(), pitch=fields.Str())
        )
        # _with(
        #     dict(dia=fields.Str(), length=fields.Str(), pitch=fields.Str())
        # )

    # def template
    def xtest_get_variant_tags(self):
        self.assertSequenceEqual(self.declaration.tags, ["dia", "length", "pitch"])

    def xtest_item_variants(self):
        """
        When a item has associated variants you can specify the options used or rely on a specific configuration
        to provide all information about a item. Then it can also specify a variant option or value to get the final config.
        """

        item = baker.make(
            "Item",
            name="Closet screws",
            declaration=self.declaration,
            configuration=self.m3,
            data=dict(
                values=dict(
                    length=52,
                )
            ),
        )

        # Description from declaration template
        self.assertEqual(item.description, "M3-0.5 x 52")

    def test_declaration_variations(self):
        pass
        # dia = range()
        # m3x10 = dict(
        #     dia=3,
        #     length=10,
        #     pitch=0.2,
        # )
        # m8x10 = dict(
        #     dia=8,
        #     length=10,
        #     pitch=1,
        # )

    # Named variants, example, some standard and then a description

    # Variation generator
    # MOdifications to the variations, if allowed
    # 5.1mm length as an example with increments of 1
    # variations


# class TestVariation(TestCase):
#     pass
