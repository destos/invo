from safedelete.managers import SafeDeleteManager
from .querysets import SituationQuerySet


class SituationManager(SafeDeleteManager):
    _queryset_class = SituationQuerySet

    def get_active(self, user):
        return self.get_queryset().filter(user=user, exit_condition=self.model.Exit.Open).latest()
