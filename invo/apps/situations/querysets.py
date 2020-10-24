# from datetime import now
import arrow
from safedelete.queryset import SafeDeleteQueryset


class SituationQuerySet(SafeDeleteQueryset):
    def _get_active_shift_kwargs(self):
        return dict(hours=-1)

    def get_active(self, user):
        """
        Get the most recently active Situation, return none if none found in criteria

        Enables situation abandonment. Removes all opened that didn't meet criteria.

        Gets the previous situation if it hasn't been abandoned or closed.
        If a certain time period has passed, will remove those open Situations.
        """

        offset = arrow.now().shift(**self._get_active_shift_kwargs()).datetime
        open_situ = self.filter(user=user, exit_condition=self.model.Exit.OPEN)

        try:
            # Also include a new dirty check? does it have a space selected?
            # Find the non-deleted open situation
            return open_situ.filter(modified__gte=offset).latest()
        except self.model.DoesNotExist:
            # Safe delete all users situations and set as abandoned
            abandoned_ids = list(open_situ.values_list("id", flat=True))
            open_situ.update(exit_condition=self.model.Exit.ABANDONED)
            # safe delete makes sure they no longer show up in default manager queries 
            self.model.objects.filter(id__in=abandoned_ids).delete()
            return None

