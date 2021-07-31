from django.contrib.sites.managers import CurrentSiteManager
from polymorphic_tree.managers import PolymorphicMPTTModelManager, PolymorphicMPTTQuerySet
from safedelete.config import DELETED_VISIBLE_BY_PK
from safedelete.managers import SafeDeleteAllManager, SafeDeleteDeletedManager, SafeDeleteManager
from safedelete.queryset import SafeDeleteQueryset


class SpaceNodeQuerySet(PolymorphicMPTTQuerySet, SafeDeleteQueryset):
    _safedelete_visibility = DELETED_VISIBLE_BY_PK
    _safedelete_visibility_field = "pk"


class SpaceNodeManager(PolymorphicMPTTModelManager, SafeDeleteManager):
    queryset_class = SpaceNodeQuerySet


class SpaceNodeAllManager(PolymorphicMPTTModelManager, SafeDeleteAllManager):
    queryset_class = SpaceNodeQuerySet


class SpaceNodeDeletedManager(PolymorphicMPTTModelManager, SafeDeleteDeletedManager):
    queryset_class = SpaceNodeQuerySet


class CurrentSiteSpaceNodeManager(CurrentSiteManager, SpaceNodeManager):
    pass
