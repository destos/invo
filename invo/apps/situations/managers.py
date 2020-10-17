from safedelete.managers import SafeDeleteManager
from .querysets import SituationQuerySet


class SituationManager(SafeDeleteManager):
    _queryset_class = SituationQuerySet
