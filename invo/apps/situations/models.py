from itertools import groupby

from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel
from django_fsm import FSMIntegerField, transition
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE, SOFT_DELETE
from polymorphic.contrib.guardian import get_polymorphic_base_content_type

from .managers import SituationManager
from spaces.models import SpaceNode
from items.models import Item


class Situation(SafeDeleteModel, TimeStampedModel):
    """
    Situations are moments when a user is interacting with the app and we want a way to continue to flow
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # TODO: through model that handles insertion order and handles manager sort?
    spaces = models.ManyToManyField(
        SpaceNode,
        through="SelectedSpace",
        through_fields=("situation", "space"),
        related_name="situations",
    )
    items = models.ManyToManyField(
        Item,
        through="SelectedItem",
        through_fields=("situation", "item"),
        related_name="situations",
    )

    # TODO: when two spaces are selected the move/swap state transition becomes available

    class States(models.IntegerChoices):
        # Starting state
        START = 0
        # Selecting items or spaces.
        SELECTING = 1
        # When you want to add a singular item
        ADDING = 2
        # When you want to place an item in a space
        PLACING = 5
        # When you want to increment an item
        INCREMENT = 3
        # When you want to consume an item
        CONSUMING = 4

    state = FSMIntegerField(default=States.START, choices=States.choices)

    class Exit(models.IntegerChoices):
        # Currently being acted on
        OPEN = 0
        # User did not interact with situation, and it was abandoned
        ABANDONED = 1
        # User completed the interaction
        COMPLETED = 2

    exit_condition = FSMIntegerField(default=Exit.OPEN, choices=Exit.choices)

    objects = SituationManager()

    class Meta(TimeStampedModel.Meta):
        ordering = ("created",)

    def __str__(self):
        return f"{self.user.username} ({self.States(self.state).label}, {self.Exit(self.exit_condition).label})"

    def __repr__(self):
        return f"<Situation: {str(self)}>"

    def has_item(self):
        return bool(self.items.exists())

    def has_space(self):
        return bool(self.spaces.exists())

    def _group_objects(self, *objects):
        manager_map = {Item: self.items, SpaceNode: self.spaces}
        for k, g in groupby(
            objects, lambda obj: get_polymorphic_base_content_type(obj).model_class()
        ):
            yield (manager_map[k], list(g))

    @transition(field=state, source=(States.START, States.SELECTING), target=States.SELECTING)
    def select(self, *selection):
        for manager, objects in self._group_objects(*selection):
            manager.add(*objects)

    @transition(field=state, source=States.SELECTING, target=States.SELECTING)
    def unselect(self, *selection):
        for manager, objects in self._group_objects(*selection):
            manager.remove(*objects)

    @transition(
        field=state, source=(States.SELECTING), target=States.ADDING, conditions=[has_space]
    )
    def chose_item(space):
        """Set situation state to adding when trying to add an item"""
        # TODO: this one is wrong, re-think it
        pass

    @transition(
        field=state, source=(States.SELECTING), target=States.PLACING, conditions=[has_item]
    )
    def chose_space(space):
        """Set situation state to placing when trying to place an item"""
        pass

    # def move_to_space(self):
    #     self.item.space = space
    #     self.item.save(update_fields=("space", "modified"))

    # def remove_from_space(self):
    #     self.item.space = None
    #     self.item.save(update_fields=("space", "modified"))


class SelectedSpace(TimeStampedModel):
    space = models.ForeignKey(SpaceNode, on_delete=models.CASCADE)
    situation = models.ForeignKey(Situation, on_delete=models.CASCADE)


class SelectedItem(TimeStampedModel):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    situation = models.ForeignKey(Situation, on_delete=models.CASCADE)


# Triggers that feed data into a situation
# queryset that returns the most recent situation for acting/adding to
