from django.test import TestCase
from model_bakery import baker
from . import models


class TestConsumable(TestCase):
    def setUp(self):
        self.item = baker.make(models.Consumable)
    
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
        self.assertNotEqual(first_modified, self.item.modified, "my default consume should update modified date")

        self.item.consume(20)
        self.assertEqual(self.item.count, 9)
        self.assertNotEqual(first_modified, self.item.modified)