from safedelete.queryset import SafeDeleteQueryset


class SituationQuerySet(SafeDeleteQueryset):
    pass
    # def get_active(self, user):
    #     return self.get(user=user)

    # Should this exist on the user? or the user sub-filters these?
    # def get_active(self):
    # return self.

    # Situation abandonment. A method that gets the previous situation if abandoned
    # Allows you to have an fresh situation if the time period has passed,
    # but get back to the previous if it was closed due to being past the normal modified
    # time period
