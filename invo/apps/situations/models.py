from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel
from django_fsm import FSMField, transition
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

from .managers import SituationManager


class Situation(SafeDeleteModel, TimeStampedModel):
    """Situations are moments when a user is interacting with the app and we want a way to continue to flow"""

    _safedelete_policy = SOFT_DELETE_CASCADE
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    space = models.ForeignKey("spaces.SpaceNode", blank=True, null=True, on_delete=models.CASCADE)
    item = models.ForeignKey("items.Item", blank=True, null=True, on_delete=models.CASCADE)
    # TODO: abandoned/canceled situation handling?

    class States(models.IntegerChoices):
        # Starting state
        START = 0
        # Selecting items or groups.
        SELECTING = 1
        # When you want to add an item
        ADDING = 2
        # When you want to place an item in a space
        PLACING = 5
        # When you want to increment an item
        INCREMENT = 3
        # When you want to consume an item
        CONSUMING = 4

    state = FSMField(default=States.START, choices=States.choices)

    objects = SituationManager()

    def has_item(self):
        return bool(self.item_id)

    def has_space(self):
        return bool(self.space_id)

    @transition(field=state, source=(States.START, States.SELECTING), target=States.SELECTING)
    def select_space(self, space):
        self.space = space

    @transition(field=state, source=(States.START, States.SELECTING), target=States.SELECTING)
    def select_item(self, item):
        self.item = item

    @transition(
        field=state, source=(States.SELECTING), target=States.ADDING, conditions=[has_space]
    )
    def chose_item(space):
        """Set situation to placing when trying to place an item"""
        # TODO: this one is wrong, re-think it
        pass

    @transition(
        field=state, source=(States.SELECTING), target=States.PLACING, conditions=[has_item]
    )
    def chose_space(space):
        """Set situation to placing when trying to place an item"""
        pass

