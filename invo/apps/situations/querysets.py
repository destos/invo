# from datetime import now
import arrow
from safedelete.queryset import SafeDeleteQueryset


class SituationQuerySet(SafeDeleteQueryset):
    def _get_active_shift_kwargs(self):
        return dict(hours=-1)

    def get_active(self, user):
        offset = arrow.now().shift(**self._get_active_shift_kwargs()).datetime
        try:
            return self.filter(
                user=user, exit_condition=self.model.Exit.OPEN, modified__gte=offset
            ).latest()
        except self.model.DoesNotExist:
            return None

    # Should this exist on the user? or the user sub-filters these?
    # def get_active(self):
    # return self.

    # Situation abandonment. A method that gets the previous situation if abandoned
    # Allows you to have an fresh situation if the time period has passed,
    # but get back to the previous if it was closed due to being past the normal modified
    # time period
