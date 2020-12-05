from polymorphic_tree.managers import PolymorphicMPTTModelManager, PolymorphicMPTTQuerySet
from safedelete.managers import SafeDeleteManager, SafeDeleteAllManager, SafeDeleteDeletedManager
from safedelete.queryset import SafeDeleteQueryset
from safedelete.config import DELETED_VISIBLE_BY_PK


class SpaceNodeQuerySet(PolymorphicMPTTQuerySet, SafeDeleteQueryset):
    _safedelete_visibility = DELETED_VISIBLE_BY_PK
    _safedelete_visibility_field = "pk"


class SpaceNodeManager(PolymorphicMPTTModelManager, SafeDeleteManager):
    queryset_class = SpaceNodeQuerySet


class SpaceNodeAllManager(PolymorphicMPTTModelManager, SafeDeleteAllManager):
    queryset_class = SpaceNodeQuerySet


class SpaceNodeDeletedManager(PolymorphicMPTTModelManager, SafeDeleteDeletedManager):
    queryset_class = SpaceNodeQuerySet
