from polymorphic.managers import PolymorphicManager

from .querysets import ItemQuerySet


class ItemManager(PolymorphicManager):
    queryset_class = ItemQuerySet

    def in_space(self, *args):
        return self.all().in_space(*args)
