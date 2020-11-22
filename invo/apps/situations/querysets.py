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

        If there is a situation in the Start state that is outside the time limit it will
        use that.
        """

        offset = arrow.now().shift(**self._get_active_shift_kwargs()).datetime
        user_situ = self.filter(user=user)
        open_situ = user_situ.filter(exit_condition=self.model.Exit.OPEN)
        clean_situ = open_situ.filter(state=self.model.States.START)

        active = None
        try:
            active = clean_situ.latest()
        except self.model.DoesNotExist:
            try:
                # Also include a new dirty check? does it have a space selected?
                # Find the non-deleted open situation
                active = open_situ.filter(modified__gte=offset).latest()
            except self.model.DoesNotExist:
                pass

        if active:
            open_situ = open_situ.exclude(id=active.id)
        # Keep ref so we can delete them after abandoned update
        abandoned_ids = list(open_situ.values_list("id", flat=True))
        # Safe delete all users situations and set as abandoned
        open_situ.update(exit_condition=self.model.Exit.ABANDONED)
        self.model.objects.filter(id__in=abandoned_ids).delete()

        return active
