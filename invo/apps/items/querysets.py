from polymorphic.managers import PolymorphicManager
from polymorphic.query import PolymorphicQuerySet

from spaces.models import SpaceNode


class ItemQuerySet(PolymorphicQuerySet):
    def in_space(self, space: SpaceNode):
        spaces = space.get_descendants(include_self=True)
        return self.filter(space__in=spaces)
