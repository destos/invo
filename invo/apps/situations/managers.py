from django.contrib.sites.managers import CurrentSiteManager
from safedelete.managers import SafeDeleteManager

from .querysets import SituationQuerySet


class SituationManager(SafeDeleteManager):
    _queryset_class = SituationQuerySet

    def get_active(self, user):
        return self.get_queryset().get_active(user)


class CurrentSiteSituationManager(CurrentSiteManager, SituationManager):
    pass
