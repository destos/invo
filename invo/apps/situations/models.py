from enum import Enum
from itertools import groupby

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from django_fsm import FSMIntegerField, transition
import ipdb
from polymorphic.contrib.guardian import get_polymorphic_base_content_type
from safedelete.models import SOFT_DELETE, SOFT_DELETE_CASCADE, SafeDeleteModel

from .managers import CurrentSiteSituationManager, SituationManager
from items.models import Item
from owners.models import SingularSite
from situations.conditions import ItemsSelected, OneSpaceSelected, SpaceSelected
from spaces.models import SpaceNode


def check_situ_conditions(*conditions):
    class Skip(Exception):
        pass

    def call(situ, **kwargs):
        condition_classes = [condition() for condition in conditions]
        try:
            for cond in condition_classes:
                if not cond.has_condition(situ):
                    raise Skip()
            for space in situ.spaces.all():
                for cond in condition_classes:
                    if not cond.has_object_condition(situ, space):
                        raise Skip()
            for space in situ.spaces.all():
                for cond in condition_classes:
                    if not cond.has_object_condition(situ, space):
                        raise Skip()
            return True
        except Skip:
            return False

    return call


class TransitionTypes(Enum):
    Selecting = 1
    Final = 2
    Exiting = 3


class Selection:
    pass


class SimpleSelection(Selection):
    conditions = (ItemsSelected & OneSpaceSelected,)
    label = _("Quick move items to selected space"),



class Situation(SingularSite, SafeDeleteModel, TimeStampedModel):
    """
    Situations are moments when a user is interacting with the app and we want a way
    to direct item and space changes with suggested actions.

    How do we drive the repercussions of situations and track what is done?
    A situation can be locked and acts as an indicator of the action that was performed.

    A deleted Situation is considered to be not acted on.

    Situations
    * When one space is selected you are given the option to select another space to move the items into
    * When two spaces are selected the move/swap state transition becomes available
    * When only two items or more are selected

    * Items moving into a space
    * Taking Items out of a space (items only selected)
    * Spaces moving into spaces, moving the nesting ( and validation )
    * Item space moving into another space. select an item, but act on the space it is inside.
    * Selected items moving into a new space

    Finished Situations

    These situations work via a rules system that given the state of the situation, presents options

    TODO: each transition needs to show a representation of the result when it is performed
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

    class States(models.IntegerChoices):
        # TODO: rethink all states
        # Starting state
        START = 0
        # Selecting items or spaces.
        SELECTING = 1
        # When you want to add a singular item
        ADDING = 2
        # When you want to place an item in a space
        PLACING = 5
        # When you want to move a space somewhere else
        MOVING = 6
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
    current_site_objects = CurrentSiteSituationManager()

    class Meta(TimeStampedModel.Meta):
        ordering = ("created",)

    def __str__(self):
        return f"{self.user} ({self.States(self.state).label}, {self.Exit(self.exit_condition).label})"

    def __repr__(self):
        return f"<Situation: {str(self)}>"

    # @classmethod
    # def __init_subclass__(cls, **kwargs):
    #     super().__init_subclass__(**kwargs)
    #     import ipdb; ipdb.set_trace()


    def _group_objects(self, *objects):
        manager_map = {Item: self.items, SpaceNode: self.spaces}
        for k, g in groupby(
            objects, lambda obj: get_polymorphic_base_content_type(obj).model_class()
        ):
            yield (manager_map[k], list(g))

    @transition(
        field=state,
        source=(States.START, States.SELECTING),
        target=States.SELECTING,
        custom=dict(type=TransitionTypes.Selecting),
    )
    def select(self, *selection):
        for manager, objects in self._group_objects(*selection):
            manager.add(*objects)

    @transition(
        field=state,
        source=States.SELECTING,
        target=States.SELECTING,
        custom=dict(type=TransitionTypes.Selecting),
    )
    def unselect(self, *selection):
        # TODO: can transition to Start? if no items selected left?
        for manager, objects in self._group_objects(*selection):
            manager.remove(*objects)

    @transition(
        field=state,
        source=(States.SELECTING),
        target=States.ADDING,
        conditions=[check_situ_conditions(ItemsSelected & OneSpaceSelected)],
        custom=dict(
            label=_("Quick move items to selected space"),
            type=TransitionTypes.Final,
            # build_proposals=
        ),
    )
    def move_items_to_space():
        "Move all items to space "
        # TODO: Perform this and log
        pass

    # @transition(
    #     field=state,
    #     source=(States.SELECTING),
    #     target=States.PLACING,
    #     custom=dict(type=TransitionTypes.Final),
    # )
    # def chose_space(space):
    #     pass

    # TODO: methods that perform movement actions on completion.

    # def move_to_space(self):
    #     self.item.space = space
    #     self.item.save(update_fields=("space", "modified"))

    # def remove_from_space(self):
    #     self.item.space = None
    #     self.item.save(update_fields=("space", "modified"))

    @property
    def available_final_transitions(self):
        # TODO: only return "final" transitions, ones that close the situation.
        def get_label(t):
            return t.__name__

        #         source_label = t.custom.get("from_state", None)
        #         label = Enum(t.name.upper()).label
        #         if source_label is None:
        #             return label
        #         state = StatusStates(self.status_state)
        #         return source_label.get(state, label)

        #     def get_direction(t):
        #         return t.custom.get("direction", TransitionDirection.FORWARD).value

        #     def get_priority(t):
        #         # A priority allows you to make transitions that can occur at the same time
        #         # appear before the other in the interface
        #         return t.custom.get("priority", 0)

        #     # TODO: get_available_user_FIELD_transitions, should be used at some point when perms are added.
        trans = self.get_available_state_transitions()
        #     Enum = self.get_status_state_transitions_enum()

        return [
            dict(
                label=get_label(t),
                # transition=Enum(t.name.upper()),
                # direction=get_direction(t),
                # priority=get_priority(t),
            )
            for t in trans
            if not t.custom.get("type", TransitionTypes.Final)
        ]


class SelectedSpace(TimeStampedModel):
    space = models.ForeignKey(SpaceNode, on_delete=models.CASCADE)
    situation = models.ForeignKey(Situation, on_delete=models.CASCADE)

    class Meta:
        ordering = ("modified",)


class SelectedItem(TimeStampedModel):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    situation = models.ForeignKey(Situation, on_delete=models.CASCADE)

    class Meta:
        ordering = ("modified",)


# Triggers that feed data into a situation
# queryset that returns the most recent situation for acting/adding to

# When selecting multiple spaces, you're given the option to consolidate all items under those spaces
# into another space
# Confirm action showing all items that are to be moved.
